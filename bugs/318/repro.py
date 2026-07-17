import os
import tempfile
from pathlib import Path

from datasets import Dataset
from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.pre_tokenizers import Whitespace
from transformers import AutoModelForCausalLM, GPT2Config, PreTrainedTokenizerFast
from trl import SFTConfig, SFTTrainer

from accelerate.big_modeling import dispatch_model
from accelerate.utils.dataclasses import FullyShardedDataParallelPlugin
from accelerate.utils.fsdp_utils import fsdp2_prepare_model


def build_tokenizer(tokenizer_dir: Path) -> PreTrainedTokenizerFast:
    vocab = {
        "<pad>": 0,
        "<eos>": 1,
        "hello": 2,
        "world": 3,
        "accelerate": 4,
        "fsdp": 5,
        "trainer": 6,
    }
    tokenizer = Tokenizer(WordLevel(vocab=vocab, unk_token="<pad>"))
    tokenizer.pre_tokenizer = Whitespace()

    fast_tokenizer = PreTrainedTokenizerFast(
        tokenizer_object=tokenizer,
        pad_token="<pad>",
        eos_token="<eos>",
    )
    fast_tokenizer.save_pretrained(tokenizer_dir)
    return fast_tokenizer


def build_model(model_dir: Path) -> None:
    config = GPT2Config(
        vocab_size=7,
        n_positions=32,
        n_ctx=32,
        n_embd=32,
        n_layer=2,
        n_head=4,
        bos_token_id=1,
        eos_token_id=1,
        pad_token_id=0,
    )
    model = AutoModelForCausalLM.from_config(config)
    model.save_pretrained(model_dir)


def main() -> None:
    if os.environ.get("CPU_FSDP_PROBE", "0") == "1":
        import torch.distributed as dist
        import torch.nn as nn

        class Block(nn.Module):
            def __init__(self, width: int):
                super().__init__()
                self.lin1 = nn.Linear(width, width)
                self.act = nn.ReLU()
                self.lin2 = nn.Linear(width, width)

            def forward(self, x):
                return self.lin2(self.act(self.lin1(x)))

        class ToyTransformer(nn.Module):
            _no_split_modules = ["Block"]

            def __init__(self, width: int = 8, depth: int = 2):
                super().__init__()
                self.embed = nn.Linear(width, width)
                self.blocks = nn.ModuleList([Block(width) for _ in range(depth)])
                self.head = nn.Linear(width, width)

            def forward(self, x):
                x = self.embed(x)
                for block in self.blocks:
                    x = block(x)
                return self.head(x)

        if not dist.is_initialized():
            dist.init_process_group("gloo")

        class FakeAccelerator:
            def __init__(self, fsdp_plugin):
                self.state = type("State", (), {"fsdp_plugin": fsdp_plugin})()
                self.mixed_precision = "no"
                self.is_main_process = dist.get_rank() == 0

        fsdp_plugin = FullyShardedDataParallelPlugin(
            fsdp_version=2,
            auto_wrap_policy="TRANSFORMER_BASED_WRAP",
            transformer_cls_names_to_wrap=["Block"],
            reshard_after_forward=True,
            state_dict_type="SHARDED_STATE_DICT",
            sync_module_states=False,
            cpu_ram_efficient_loading=False,
            activation_checkpointing=True,
        )
        fake_accelerator = FakeAccelerator(fsdp_plugin)
        print(f"cpu_probe_rank={dist.get_rank()} world_size={dist.get_world_size()}")
        fsdp2_prepare_model(fake_accelerator, ToyTransformer())
        print("cpu_probe_prepare_completed")
        return

    with tempfile.TemporaryDirectory(prefix="fsdp2_sft_") as workdir:
        workdir_path = Path(workdir)
        tokenizer_dir = workdir_path / "tokenizer"
        model_dir = workdir_path / "model"
        output_dir = workdir_path / "out"
        tokenizer_dir.mkdir()
        model_dir.mkdir()
        output_dir.mkdir()

        tokenizer = build_tokenizer(tokenizer_dir)
        build_model(model_dir)

        # The issue report loads the model with `device_map="auto"` before handing it to SFTTrainer.
        # For this tiny local model, dispatch explicitly so the model carries the same device-map metadata.
        model = AutoModelForCausalLM.from_pretrained(model_dir)
        model = dispatch_model(model, device_map={"": 0})
        dataset = Dataset.from_dict({"text": ["hello world", "accelerate fsdp trainer"]})

        training_args = SFTConfig(
            output_dir=str(output_dir),
            per_device_train_batch_size=1,
            gradient_accumulation_steps=1,
            num_train_epochs=1,
            logging_steps=1,
            report_to="none",
            bf16=True,
            max_length=16,
            dataset_text_field="text",
            packing=False,
            use_cpu=False,
            do_train=True,
        )

        print(f"cuda_visible={os.environ.get('CUDA_VISIBLE_DEVICES', 'all')}")
        print(f"world_size={os.environ.get('WORLD_SIZE', '1')}")
        print(f"model_device_map={getattr(model, 'hf_device_map', None)}")

        trainer = SFTTrainer(
            model=model,
            args=training_args,
            train_dataset=dataset,
            processing_class=tokenizer,
        )
        trainer.train()


if __name__ == "__main__":
    main()

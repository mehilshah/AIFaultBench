import tempfile
import traceback
from pathlib import Path
import sys

import torch


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

from transformers import CanineConfig, CanineModel  # noqa: E402
import transformers  # noqa: E402


class CanineWrapper(torch.nn.Module):
    def __init__(self):
        super().__init__()
        config = CanineConfig(
            hidden_size=32,
            num_hidden_layers=1,
            num_attention_heads=4,
            intermediate_size=64,
            max_position_embeddings=256,
        )
        self.model = CanineModel(config)

    def forward(self, input_ids, attention_mask):
        return self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            return_dict=True,
        ).last_hidden_state


def main():
    print("torch:", torch.__version__)
    print("transformers:", transformers.__version__)

    model = CanineWrapper().eval().half()

    input_ids = torch.randint(
        low=0,
        high=256,
        size=(1, 64),
        dtype=torch.long,
    )
    attention_mask = torch.ones(
        1,
        64,
        dtype=torch.long,
    )

    output_path = Path(tempfile.gettempdir()) / "canine_fp16_repro.onnx"
    print("exporting to:", output_path)

    try:
        torch.onnx.export(
            model,
            (input_ids, attention_mask),
            str(output_path),
            input_names=["input_ids", "attention_mask"],
            output_names=["last_hidden_state"],
            opset_version=18,
            do_constant_folding=True,
            dynamo=False,
        )
        print("onnx export succeeded")
    except Exception:
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()

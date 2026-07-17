from pathlib import Path
import sys

import torch


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

from x_transformers import Decoder, TransformerWrapper


def main() -> None:
    lm = TransformerWrapper(
        num_tokens=32,
        max_seq_len=0,
        num_memory_tokens=20,
        attn_layers=Decoder(
            dim=512,
            depth=4,
            heads=4,
            rotary_pos_emb=True,
            attn_flash=True,
            attn_onnxable=True,
            attn_num_mem_kv=20,
            attn_one_kv_head=True,
        ),
    )

    x = torch.randint(0, 32, (8, 1024))
    logits = lm(x)
    print(x.shape, x.dtype)
    print(logits.shape, logits.dtype)


if __name__ == "__main__":
    main()

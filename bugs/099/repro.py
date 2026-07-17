import os
import sys

import torch


ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "codebase"))

from rotary_embedding_torch import RotaryEmbedding


def run_case(dtype):
    emb = RotaryEmbedding(dim=32).cuda()
    q = torch.randn(2, 4, 8, 32, device="cuda", dtype=torch.float32).to(dtype)
    out = emb.rotate_queries_or_keys(q)
    finite = torch.isfinite(out.float()).all().item()
    print(f"dtype={dtype}, output_dtype={out.dtype}, finite={finite}")


def main():
    print(f"torch={torch.__version__}")
    print(f"cuda_available={torch.cuda.is_available()}")

    run_case(torch.float16)
    run_case(torch.float8_e4m3fn)


if __name__ == "__main__":
    main()

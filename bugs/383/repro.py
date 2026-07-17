#!/usr/bin/env python3
import os
import sys


def main() -> None:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    codebase_path = os.path.join(repo_root, "codebase")
    sys.path.insert(0, codebase_path)

    import torch
    import timm
    from torch.distributed.fsdp._fully_shard._fully_shard import fully_shard

    print(f"python={sys.version.split()[0]}")
    print(f"torch={torch.__version__}")
    print(f"timm={timm.__version__}")

    encoder = timm.create_model(
        "convnextv2_base",
        pretrained=False,
        features_only=True,
    )
    print(f"model_type={type(encoder).__name__}")

    try:
        fully_shard(encoder)
    except Exception as exc:
        print(f"exception_type={type(exc).__name__}")
        print(f"exception_message={exc}")
        raise

    print("fully_shard succeeded unexpectedly")


if __name__ == "__main__":
    main()

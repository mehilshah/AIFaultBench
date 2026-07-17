import torch_geometric


def main() -> None:
    print(f"torch_geometric_version={torch_geometric.__version__}")
    print(f"has_HashTensor={hasattr(torch_geometric, 'HashTensor')}")
    from torch_geometric import HashTensor  # noqa: F401


if __name__ == "__main__":
    main()

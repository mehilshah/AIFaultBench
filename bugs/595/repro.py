import importlib
import importlib.util
import sys
import traceback


def block_torchvision_imports():
    real_find_spec = importlib.util.find_spec
    real_import_module = importlib.import_module

    def blocked_find_spec(name, package=None):
        if name == "torchvision" or name.startswith("torchvision."):
            return None
        return real_find_spec(name, package)

    def blocked_import_module(name, package=None):
        if name == "torchvision" or name.startswith("torchvision."):
            raise ModuleNotFoundError("No module named 'torchvision'")
        return real_import_module(name, package)

    importlib.util.find_spec = blocked_find_spec
    importlib.import_module = blocked_import_module


def main():
    block_torchvision_imports()

    import torch
    from transformers import AutoProcessor

    model_id = "HuggingFaceTB/SmolVLM-256M-Instruct"

    print(f"torch={torch.__version__}")
    print("torchvision=blocked")
    print(f"model_id={model_id}")

    try:
        processor = AutoProcessor.from_pretrained(model_id)
        print(f"loaded_processor={type(processor).__name__}")
        return 0
    except Exception as exc:
        print(f"exception_type={type(exc).__name__}")
        print(f"exception_message={exc}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

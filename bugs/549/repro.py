from pathlib import Path
import sys
import traceback

import torch


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

import timm  # noqa: E402
from timm.utils.onnx import onnx_export  # noqa: E402


def main() -> None:
    model_name = "bat_resnext26ts.ch_in1k"
    output_file = ROOT / f"{model_name}.onnx"

    print(f"torch={torch.__version__}")
    print(f"has_torch_onnx__export={hasattr(torch.onnx, '_export')}")
    print(f"model={model_name}")

    model = timm.create_model(model_name, exportable=True)
    model.eval()

    onnx_export(model=model, output_file=str(output_file))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        raise

import sys

import torch

import timm


def run() -> int:
    torch.manual_seed(0)

    print(f"python={sys.version.split()[0]}")
    print(f"timm={timm.__version__}")
    print(f"torch={torch.__version__}")

    model = timm.create_model("swinv2_cr_tiny_224", pretrained=False, features_only=True)
    model.eval()
    print(f"default_input_size={model.default_cfg.get('input_size')}")

    with torch.no_grad():
        out_224 = model(torch.randn(1, 3, 224, 224))
        print("224_ok=", [tuple(t.shape) for t in out_224])

        try:
            model(torch.randn(1, 3, 512, 512))
        except Exception as exc:  # noqa: BLE001 - capture the exact runtime failure
            print(f"512_error={type(exc).__name__}: {exc}")
            if "Input image height (512) doesn't match model (224)." in str(exc):
                print("BUG_REPRODUCED")
                return 0
            return 1

    print("UNEXPECTED_SUCCESS")
    return 1


if __name__ == "__main__":
    raise SystemExit(run())

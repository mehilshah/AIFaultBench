from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "codebase" / "src" / "diffusers" / "loaders" / "lora_conversion_utils.py"


def load_target_module():
    """Load the pinned source file while stubbing the tiny diffusers surface it imports."""
    diffusers_pkg = types.ModuleType("diffusers")
    diffusers_pkg.__path__ = [str(TARGET.parents[1])]

    loaders_pkg = types.ModuleType("diffusers.loaders")
    loaders_pkg.__path__ = [str(TARGET.parent)]

    utils_pkg = types.ModuleType("diffusers.utils")

    class _Logging:
        @staticmethod
        def get_logger(name):
            class _Logger:
                def info(self, *args, **kwargs):
                    pass

                def warning(self, *args, **kwargs):
                    pass

                def debug(self, *args, **kwargs):
                    pass

            return _Logger()

    utils_pkg.logging = _Logging()
    utils_pkg.is_peft_version = lambda *args, **kwargs: False
    utils_pkg.state_dict_all_zero = lambda *args, **kwargs: False

    sys.modules["diffusers"] = diffusers_pkg
    sys.modules["diffusers.loaders"] = loaders_pkg
    sys.modules["diffusers.utils"] = utils_pkg

    spec = importlib.util.spec_from_file_location("diffusers.loaders.lora_conversion_utils", TARGET)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def kohya(name: str, out: int, inp: int, rank: int = 4, alpha: bool = True):
    state = {
        f"{name}.lora_down.weight": torch.zeros(rank, inp),
        f"{name}.lora_up.weight": torch.zeros(out, rank),
    }
    if alpha:
        state[f"{name}.alpha"] = torch.tensor(float(rank))
    return state


def base_state(rank: int = 4, hid: int = 3072):
    return kohya("lora_unet_double_blocks_0_img_attn_proj", hid, hid, rank=rank)


def main() -> int:
    module = load_target_module()
    convert = module._convert_kohya_flux_lora_to_diffusers

    cases = [
        (
            "case_a",
            base_state() | kohya("lora_unet_final_layer_linear", 64, 3072, alpha=False),
            "KeyError",
            "lora_unet_final_layer_adaLN_modulation_1.lora_down.weight",
        ),
        (
            "case_b",
            base_state()
            | kohya("lora_unet_final_layer_linear", 64, 3072)
            | kohya("lora_unet_final_layer_adaLN_modulation_1", 6144, 3072),
            "ValueError",
            "Incompatible keys detected",
        ),
    ]

    observed = []
    for label, state_dict, expected_exc, expected_text in cases:
        try:
            convert(state_dict)
        except Exception as exc:  # noqa: BLE001
            message = str(exc)
            print(f"{label}: {type(exc).__name__}: {message}")
            observed.append((label, type(exc).__name__, message))
        else:
            print(f"{label}: unexpectedly succeeded")
            return 1

    case_a_ok = any(
        label == "case_a" and exc_name == "KeyError" and "lora_unet_final_layer_adaLN_modulation_1.lora_down.weight" in message
        for label, exc_name, message in observed
    )
    case_b_ok = any(
        label == "case_b" and exc_name == "ValueError" and "Incompatible keys detected" in message and "alpha" in message
        for label, exc_name, message in observed
    )

    if case_a_ok and case_b_ok:
        print("reproduced: yes")
        return 0

    print("reproduced: no")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

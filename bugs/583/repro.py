#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import logging as pylogging
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODULE_PATH = ROOT / "codebase" / "src" / "diffusers" / "utils" / "dynamic_modules_utils.py"
RESULT_PATH = ROOT / "reproduction.json"


def load_dynamic_modules_utils():
    """Load the target module without importing the full diffusers package."""
    diffusers_pkg = types.ModuleType("diffusers")
    diffusers_pkg.__version__ = "0.39.0.dev0"

    utils_pkg = types.ModuleType("diffusers.utils")
    utils_pkg.DIFFUSERS_DYNAMIC_MODULE_NAME = "diffusers_modules"
    utils_pkg.HF_MODULES_CACHE = "/tmp/hf_modules_cache_repro_583"
    utils_pkg.logging = types.SimpleNamespace(get_logger=pylogging.getLogger)

    constants_pkg = types.ModuleType("diffusers.utils.constants")
    constants_pkg.DIFFUSERS_DISABLE_REMOTE_CODE = False

    sys.modules["diffusers"] = diffusers_pkg
    sys.modules["diffusers.utils"] = utils_pkg
    sys.modules["diffusers.utils.constants"] = constants_pkg

    spec = importlib.util.spec_from_file_location("diffusers.utils.dynamic_modules_utils", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module spec from {MODULE_PATH}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_case(module, model_id: str, module_file: str = "pipeline.py"):
    try:
        value = module.get_cached_module_file(
            pretrained_model_name_or_path=model_id,
            module_file=module_file,
            trust_remote_code=False,
        )
        return {"model_id": model_id, "raised": False, "value": value}
    except Exception as exc:  # noqa: BLE001
        return {
            "model_id": model_id,
            "raised": True,
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
        }


def main() -> int:
    module = load_dynamic_modules_utils()

    control = run_case(module, "hf-internal-testing/diffusers-dummy-pipeline")
    vulnerable = run_case(module, "clip_guided_stable_diffusion")

    reproducible = control["raised"] and not vulnerable["raised"] and vulnerable["value"].endswith(
        "diffusers_modules/git/clip_guided_stable_diffusion.py"
    )

    result = {
        "reproducible": reproducible,
        "evidence": (
            "Control case raised ValueError for a normal remote repo, but the community pipeline "
            "case returned diffusers_modules/git/clip_guided_stable_diffusion.py with trust_remote_code=False."
        ),
        "steps": [
            "Load diffusers/utils/dynamic_modules_utils.py directly with a minimal stub package.",
            "Call get_cached_module_file() for hf-internal-testing/diffusers-dummy-pipeline with trust_remote_code=False and observe ValueError.",
            "Call get_cached_module_file() for clip_guided_stable_diffusion with trust_remote_code=False and observe it returns a cached module path instead of raising.",
        ],
        "blocking_reason": "" if reproducible else "The community pipeline branch did not bypass the trust check in this environment.",
        "reproduction_command": "bash run_repro.sh",
    }

    print(json.dumps({"control": control, "vulnerable": vulnerable}, indent=2))
    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    return 0 if reproducible else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Reproduce timm's Hugging Face hub cache miss behavior.

This harness loads the relevant `codebase/timm/models/_hub.py` module directly
from source, replaces the hub download function with a controllable fake, and
invokes `load_state_dict_from_hf()` twice with a cache directory that already
contains the target file.

Expected behavior for a cache-aware loader:
  - The first call downloads the file.
  - The second call reuses the cached file without re-contacting the hub.

Actual behavior in this code path:
  - `hf_hub_download()` is invoked again on the second call, which is where
    a real user would hit Hugging Face rate limiting.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
import tempfile
import types
from contextlib import contextmanager
from dataclasses import asdict


ROOT = pathlib.Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
RESULT_JSON = ROOT / "reproduction.json"


def _write_json(payload: dict) -> None:
    RESULT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


@contextmanager
def _prepend_sys_path(path: pathlib.Path):
    sys.path.insert(0, str(path))
    try:
        yield
    finally:
        try:
            sys.path.remove(str(path))
        except ValueError:
            pass


def _install_fake_torch() -> None:
    fake_torch = types.ModuleType("torch")
    fake_torch.load = lambda *args, **kwargs: {"dummy": 1}
    fake_torch.Tensor = type("Tensor", (), {})
    fake_torch.nn = types.SimpleNamespace(Module=type("Module", (), {}))

    fake_hub = types.ModuleType("torch.hub")
    fake_hub.HASH_REGEX = __import__("re").compile(r"([a-f0-9]{8})")
    fake_hub.download_url_to_file = lambda *args, **kwargs: None
    fake_hub.get_dir = lambda: tempfile.gettempdir()
    fake_hub._get_torch_home = lambda: tempfile.gettempdir()
    fake_hub.urlparse = __import__("urllib.parse", fromlist=["urlparse"]).urlparse
    fake_torch.hub = fake_hub

    sys.modules["torch"] = fake_torch
    sys.modules["torch.hub"] = fake_hub


def _load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    temp_root = pathlib.Path(tempfile.mkdtemp(prefix="timm_hf_cache_repro_"))
    cache_dir = temp_root / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Force `import safetensors.torch` inside `_hub.py` to fail so the test
    # focuses on the pytorch checkpoint path only.
    with tempfile.TemporaryDirectory(prefix="timm_safetensors_stub_") as stub_dir_str:
        stub_dir = pathlib.Path(stub_dir_str)
        (stub_dir / "safetensors.py").write_text('raise ImportError("disabled for repro")\n')

        _install_fake_torch()

        # Minimal `timm` package skeleton so `_hub.py` can import `timm.__version__`.
        timm_pkg = types.ModuleType("timm")
        timm_pkg.__path__ = [str(CODEBASE / "timm")]
        timm_pkg.__version__ = "repro"
        sys.modules["timm"] = timm_pkg

        timm_version = types.ModuleType("timm.version")
        timm_version.__version__ = "repro"
        sys.modules["timm.version"] = timm_version

        with _prepend_sys_path(stub_dir):
            pretrained_mod = _load_module(
                "timm.models._pretrained", CODEBASE / "timm/models/_pretrained.py"
            )
            hub_mod = _load_module("timm.models._hub", CODEBASE / "timm/models/_hub.py")

        calls = []
        target_file = cache_dir / hub_mod.HF_WEIGHTS_NAME

        def fake_hf_hub_download(repo_id, filename, revision=None, cache_dir=None, **kwargs):
            call_no = len(calls) + 1
            calls.append(
                {
                    "call_no": call_no,
                    "repo_id": repo_id,
                    "filename": filename,
                    "revision": revision,
                    "cache_dir": str(cache_dir) if cache_dir is not None else None,
                }
            )
            if call_no == 1:
                pathlib.Path(cache_dir).mkdir(parents=True, exist_ok=True)
                pathlib.Path(cache_dir, filename).write_text("cached checkpoint placeholder\n")
                return str(pathlib.Path(cache_dir, filename))
            raise RuntimeError("Simulated Hugging Face rate limit: second hub call was made")

        hub_mod.hf_hub_download = fake_hf_hub_download

        # First load succeeds and populates the cache.
        first_state = hub_mod.load_state_dict_from_hf(
            "MahmoodLab/uni",
            filename=hub_mod.HF_WEIGHTS_NAME,
            cache_dir=cache_dir,
        )

        print(f"first_load_ok={bool(first_state)}")
        print(f"cache_file_exists_after_first_load={target_file.exists()}")

        # Second load should not need another hub call if the loader consulted
        # the local cache before reaching out. The current code does reach out.
        try:
            hub_mod.load_state_dict_from_hf(
                "MahmoodLab/uni",
                filename=hub_mod.HF_WEIGHTS_NAME,
                cache_dir=cache_dir,
            )
        except Exception as exc:
            print(f"second_load_exception={type(exc).__name__}: {exc}")
            print(f"hub_call_count={len(calls)}")
            _write_json(
                {
                    "reproducible": True,
                    "evidence": (
                        "The second load called the fake hf_hub_download again even though "
                        f"{target_file} already existed, and the call failed with: {type(exc).__name__}: {exc}"
                    ),
                    "steps": [
                        "Load timm.models._hub from the local codebase with fake torch and safetensors stubs.",
                        "Call load_state_dict_from_hf('MahmoodLab/uni') once to populate the cache directory.",
                        "Call it again with the same cache directory and observe that hf_hub_download is invoked a second time.",
                    ],
                    "blocking_reason": "",
                    "reproduction_command": "bash run_repro.sh",
                }
            )
            return 1

        print(f"hub_call_count={len(calls)}")
        _write_json(
            {
                "reproducible": False,
                "evidence": "Unexpectedly no second hub call was made.",
                "steps": [
                    "Load timm.models._hub from the local codebase with fake torch and safetensors stubs.",
                    "Call load_state_dict_from_hf('MahmoodLab/uni') twice using the same cache directory.",
                ],
                "blocking_reason": "The expected second hub call did not happen in this run.",
                "reproduction_command": "bash run_repro.sh",
            }
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(main())

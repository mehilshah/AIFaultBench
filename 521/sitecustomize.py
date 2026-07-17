"""Startup compatibility patches for the repro environment.

The current transformers checkout expects a few huggingface_hub APIs that are not
present in the wheel version we can install in this environment. Patch them here
so the repro can exercise the model code without mutating the codebase.
"""

from __future__ import annotations

import importlib.metadata


_orig_version = importlib.metadata.version


def _patched_version(name: str) -> str:
    if name == "tokenizers":
        return "0.23.0"
    if name in {"huggingface-hub", "huggingface_hub"}:
        return "1.24.0"
    return _orig_version(name)


importlib.metadata.version = _patched_version

try:
    import huggingface_hub

    if not hasattr(huggingface_hub, "is_offline_mode"):
        huggingface_hub.is_offline_mode = lambda: False

    try:
        from huggingface_hub import dataclasses as _hf_dataclasses

        if not hasattr(_hf_dataclasses, "validate_typed_dict"):
            def validate_typed_dict(*args, **kwargs):
                return None

            _hf_dataclasses.validate_typed_dict = validate_typed_dict

        def _identity_strict(cls=None, *, accept_kwargs=False):
            if cls is None:
                return lambda x: x
            return cls

        _hf_dataclasses.strict = _identity_strict
        huggingface_hub.strict = _identity_strict
    except Exception:
        pass
except Exception:
    pass

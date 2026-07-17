"""Minimal safetensors stub so diffusers can import its loading helpers without the real package."""

from __future__ import annotations

from . import torch as torch  # noqa: F401


class SafetensorError(Exception):
    pass


class _SafeOpen:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def keys(self):
        return []


def safe_open(*args, **kwargs):
    return _SafeOpen(*args, **kwargs)

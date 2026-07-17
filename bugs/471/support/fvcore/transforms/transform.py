"""Minimal fvcore transform stubs for the repro harness."""

from __future__ import annotations


class Transform:
    def __init__(self):
        pass

    def _set_attributes(self, locals_dict):
        for key, value in locals_dict.items():
            if key != "self":
                setattr(self, key, value)

    @classmethod
    def register_type(cls, name, func):
        return func


class TransformList(list):
    pass


class HFlipTransform(Transform):
    def __init__(self, width=None):
        super().__init__()
        self.width = width


class NoOpTransform(Transform):
    pass


class CropTransform(Transform):
    def __init__(self, x0, y0, w, h):
        super().__init__()
        self.x0 = x0
        self.y0 = y0
        self.w = w
        self.h = h


class BlendTransform(Transform):
    pass

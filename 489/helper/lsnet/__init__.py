"""Tiny stand-in for an external custom model package.

The real issue report references a custom `lsnet` package. The important bit is
that the model must be imported so its `@register_model` side effect runs.
"""

from __future__ import annotations

from torch import nn

from timm.models import register_model


class LSNetTiny(nn.Module):
    def __init__(self, num_classes: int = 1000, **kwargs):
        super().__init__()
        self.num_classes = num_classes
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.flatten = nn.Flatten(1)
        self.head = nn.Linear(3, num_classes)

    def forward(self, x):
        x = self.pool(x)
        x = self.flatten(x)
        return self.head(x)


@register_model
def lsnet_t(pretrained: bool = False, **kwargs):
    del pretrained
    return LSNetTiny(**kwargs)

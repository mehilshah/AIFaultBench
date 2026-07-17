from __future__ import annotations

from types import SimpleNamespace

import torch
import torch.nn.functional as F


class Params4bit(torch.nn.Parameter):
    def __new__(cls, data=None, requires_grad=False, **kwargs):
        if data is None:
            data = torch.empty(0)
        return torch.nn.Parameter.__new__(cls, data, requires_grad=requires_grad)


class Int8Params(torch.nn.Parameter):
    def __new__(cls, data=None, requires_grad=False, **kwargs):
        if data is None:
            data = torch.empty(0)
        return torch.nn.Parameter.__new__(cls, data, requires_grad=requires_grad)


class Linear4bit(torch.nn.Linear):
    def __init__(
        self,
        in_features,
        out_features,
        bias=True,
        compute_dtype=None,
        compress_statistics=False,
        quant_type="nf4",
        quant_storage=torch.float32,
        **kwargs,
    ):
        super().__init__(in_features, out_features, bias=bias)
        self.compute_dtype = compute_dtype or torch.float32
        self.compress_statistics = compress_statistics
        self.quant_type = quant_type
        self.weight = Params4bit(torch.zeros(1, 1, dtype=quant_storage), requires_grad=False)
        self.weight.quant_state = SimpleNamespace()
        self.weight.compress_statistics = compress_statistics
        self.weight.quant_type = quant_type
        self.weight.bnb_quantized = True
        self.state = SimpleNamespace(SCB=None, CxB=None, SB=None, formatB=None, reset_grads=lambda: None)
        self.true_weight = torch.randn(out_features, in_features) * 0.01

    def forward(self, x, *args, **kwargs):
        return F.linear(x, self.true_weight.to(dtype=x.dtype, device=x.device), self.bias)


class Linear8bitLt(torch.nn.Linear):
    def __init__(self, in_features, out_features, bias=True, **kwargs):
        super().__init__(in_features, out_features, bias=bias)
        self.weight = Int8Params(torch.zeros(out_features, in_features), requires_grad=False)
        self.state = SimpleNamespace(SCB=None, CxB=None, SB=None, formatB=None, reset_grads=lambda: None)
        self.true_weight = torch.randn(out_features, in_features) * 0.01

    def forward(self, x, *args, **kwargs):
        return F.linear(x, self.true_weight.to(dtype=x.dtype, device=x.device), self.bias)

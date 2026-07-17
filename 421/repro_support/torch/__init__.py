"""Lightweight torch stub used to import the diffusers source tree without the broken system torch binary."""

from __future__ import annotations

import sys
import types
from contextlib import ContextDecorator
from dataclasses import dataclass

__version__ = "2.3.0"
__path__ = []  # Makes this module behave like a package for submodule imports.


class _DType(str):
    pass


dtype = _DType
layout = type("layout", (), {})

float16 = _DType("float16")
float32 = _DType("float32")
bfloat16 = _DType("bfloat16")
float64 = _DType("float64")
float8_e4m3fn = _DType("float8_e4m3fn")
float8_e5m2 = _DType("float8_e5m2")
int8 = _DType("int8")
uint8 = _DType("uint8")
int16 = _DType("int16")
uint16 = _DType("uint16")
int32 = _DType("int32")
int64 = _DType("int64")
long = int64
bool = _DType("bool")
strided = object()


@dataclass
class device:
    type: str
    index: int | None = None

    def __init__(self, value="cpu", index=None):
        if isinstance(value, device):
            self.type = value.type
            self.index = value.index if index is None else index
            return
        if isinstance(value, str) and ":" in value:
            self.type, index_text = value.split(":", 1)
            self.index = int(index_text)
        else:
            self.type = str(value)
            self.index = index

    def __str__(self):
        return f"{self.type}:{self.index}" if self.index is not None else self.type


class Tensor:
    def __init__(self, *args, **kwargs):
        self.shape = kwargs.pop("shape", ())
        self.dtype = kwargs.pop("dtype", float32)
        self.device = kwargs.pop("device", device("cpu"))

    def to(self, *args, **kwargs):
        return self

    def view(self, *shape):
        self.shape = tuple(shape)
        return self

    def reshape(self, *shape):
        self.shape = tuple(shape)
        return self

    def permute(self, *dims):
        return self

    def cpu(self):
        self.device = device("cpu")
        return self

    def numpy(self):
        return []

    def item(self):
        return 0


class Generator:
    def __init__(self, device="cpu"):
        self.device = device if isinstance(device, device) else globals()["device"](device)


class _NoGrad(ContextDecorator):
    def __call__(self, fn):
        return fn

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def no_grad():
    return _NoGrad()


def tensor(data, *args, **kwargs):
    return Tensor(shape=getattr(data, "shape", (len(data),) if hasattr(data, "__len__") else ()), **kwargs)


def zeros(shape, *args, **kwargs):
    return Tensor(shape=tuple(shape), **kwargs)


def ones(shape, *args, **kwargs):
    return Tensor(shape=tuple(shape), **kwargs)


def randn(shape, *args, **kwargs):
    return Tensor(shape=tuple(shape), **kwargs)


def arange(*args, **kwargs):
    return Tensor(shape=(0,), **kwargs)


def cat(tensors, dim=0):
    return Tensor(shape=getattr(tensors[0], "shape", ()), device=getattr(tensors[0], "device", device("cpu")))


def stack(tensors, dim=0):
    return Tensor(shape=getattr(tensors[0], "shape", ()), device=getattr(tensors[0], "device", device("cpu")))


def sqrt(x):
    return x


def manual_seed(seed):
    return seed


class Module:
    def __init__(self, *args, **kwargs):
        self.training = True

    def forward(self, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        if hasattr(self, "forward"):
            return self.forward(*args, **kwargs)
        return None

    def to(self, *args, **kwargs):
        return self

    def cuda(self, *args, **kwargs):
        return self

    def cpu(self, *args, **kwargs):
        return self

    def half(self):
        return self

    def float(self):
        return self

    def eval(self):
        self.training = False
        return self

    def train(self, mode=True):
        self.training = mode
        return self

    def modules(self):
        yield self

    def named_modules(self):
        yield "", self

    def named_children(self):
        return iter(())

    def children(self):
        return iter(())

    def parameters(self):
        return iter(())

    def state_dict(self):
        return {}


class Parameter(Tensor):
    pass


nn = types.ModuleType("torch.nn")
nn.__path__ = []  # type: ignore[attr-defined]
nn.Module = Module
nn.Parameter = Parameter
nn.ModuleList = list
nn.ModuleDict = dict
nn.Identity = Module
nn.Linear = Module
nn.Conv2d = Module
nn.init = types.ModuleType("torch.nn.init")
for _name in [
    "uniform_",
    "normal_",
    "trunc_normal_",
    "constant_",
    "xavier_uniform_",
    "xavier_normal_",
    "kaiming_uniform_",
    "kaiming_normal_",
    "uniform",
    "normal",
    "xavier_uniform",
    "xavier_normal",
    "kaiming_uniform",
    "kaiming_normal",
]:
    setattr(nn.init, _name, lambda *args, **kwargs: None)
sys.modules[__name__ + ".nn.init"] = nn.init
sys.modules[__name__ + ".nn"] = nn


def _make_simple_backend(name: str):
    backend = types.ModuleType(f"torch.{name}")
    backend.empty_cache = lambda: None
    backend.device_count = lambda: 0
    backend.manual_seed = lambda seed=None: seed
    backend.reset_peak_memory_stats = lambda *args, **kwargs: None
    backend.reset_max_memory_allocated = lambda *args, **kwargs: None
    backend.max_memory_allocated = lambda *args, **kwargs: 0
    backend.synchronize = lambda *args, **kwargs: None
    backend.is_available = lambda: False
    sys.modules[__name__ + f".{name}"] = backend
    return backend


cuda = _make_simple_backend("cuda")
xpu = _make_simple_backend("xpu")
mps = _make_simple_backend("mps")


fft = types.ModuleType("torch.fft")
fft.fftn = lambda *args, **kwargs: args[0] if args else None
fft.fftshift = lambda *args, **kwargs: args[0] if args else None
fft.ifftn = lambda *args, **kwargs: args[0] if args else None
fft.ifftshift = lambda *args, **kwargs: args[0] if args else None
sys.modules[__name__ + ".fft"] = fft


_dynamo = types.ModuleType("torch._dynamo")
_dynamo.allow_in_graph = lambda cls: cls
sys.modules[__name__ + "._dynamo"] = _dynamo


utils = types.ModuleType("torch.utils")
utils.__path__ = []  # type: ignore[attr-defined]
_pytree = types.ModuleType("torch.utils._pytree")
_pytree._dict_flatten = lambda d: (list(d.values()), list(d.keys()))
_pytree._dict_unflatten = lambda values, context: dict(zip(context, values))
_pytree.register_pytree_node = lambda *args, **kwargs: None
_pytree._register_pytree_node = lambda *args, **kwargs: None
checkpoint = types.ModuleType("torch.utils.checkpoint")
checkpoint.checkpoint = lambda fn, *args, **kwargs: fn(*args, **kwargs)
utils._pytree = _pytree
utils.checkpoint = checkpoint
sys.modules[__name__ + ".utils"] = utils
sys.modules[__name__ + ".utils._pytree"] = _pytree
sys.modules[__name__ + ".utils.checkpoint"] = checkpoint


distributed = types.ModuleType("torch.distributed")
distributed.__path__ = []  # type: ignore[attr-defined]
distributed.is_available = lambda: False
distributed.is_initialized = lambda: False
distributed.get_rank = lambda: 0
distributed.get_world_size = lambda: 1
distributed.barrier = lambda *args, **kwargs: None
distributed.get_backend = lambda *args, **kwargs: "gloo"
distributed.all_gather = lambda *args, **kwargs: None
distributed.ProcessGroup = type("ProcessGroup", (), {})
distributed.Backend = type("Backend", (), {})
distributed.ReduceOp = type("ReduceOp", (), {})
distributed.Store = type("Store", (), {})
distributed.Work = type("Work", (), {})
distributed.device_mesh = types.ModuleType("torch.distributed.device_mesh")
distributed.device_mesh.DeviceMesh = type("DeviceMesh", (), {})
sys.modules[__name__ + ".distributed"] = distributed
sys.modules[__name__ + ".distributed.device_mesh"] = distributed.device_mesh


def __getattr__(name):
    # Keep imports resilient when the source tree asks for an unimplemented torch symbol.
    if name == "dtype":
        return dtype
    if name == "layout":
        return layout

    class _TorchMissing:
        def __init__(self, symbol_name: str):
            self.__name__ = f"torch.{symbol_name}"
            self.symbol_name = symbol_name

        def __call__(self, *args, **kwargs):
            return self

        def __getattr__(self, item):
            return self

        def __hash__(self):
            return hash(self.symbol_name)

        def __eq__(self, other):
            return isinstance(other, _TorchMissing) and self.symbol_name == other.symbol_name

        def __repr__(self):
            return self.__name__

    sentinel = _TorchMissing(name)
    setattr(sys.modules[__name__], name, sentinel)
    return sentinel

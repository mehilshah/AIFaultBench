"""Minimal torch shim for the Lightning xpu accelerator repro.

This project snapshot has a broken binary torch install in the execution
environment. The shim provides just enough surface area for Lightning to import
and reach the accelerator-name validation path.
"""

from __future__ import annotations

from dataclasses import dataclass
import sys
import types
from typing import Any

__version__ = "2.5.0"


@dataclass(frozen=True)
class device:
    type: str = "cpu"
    index: int | None = None

    def __repr__(self) -> str:
        if self.index is None:
            return f"device(type='{self.type}')"
        return f"device(type='{self.type}', index={self.index})"


class Tensor:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._args = args
        self._kwargs = kwargs

    def size(self, dim: int | None = None) -> int | tuple[int, ...]:
        return 0 if dim is not None else ()

    def view(self, *_args: Any, **_kwargs: Any) -> "Tensor":
        return self

    def to(self, *_args: Any, **_kwargs: Any) -> "Tensor":
        return self

    def relu(self) -> "Tensor":
        return self

    def __iter__(self):
        return iter(())


class _DType:
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"torch.{self.name}"


def _make_module(name: str) -> types.ModuleType:
    module = types.ModuleType(name)
    module.__path__ = []  # type: ignore[attr-defined]

    def __getattr__(attr: str) -> Any:
        placeholder = types.SimpleNamespace(__name__=f"{name}.{attr}")
        return placeholder

    module.__getattr__ = __getattr__  # type: ignore[attr-defined]
    return module


def _register_module(name: str, module: types.ModuleType) -> types.ModuleType:
    sys.modules[name] = module
    return module


def _noop(*_args: Any, **_kwargs: Any) -> Any:
    return None


def _return_first(arg: Any, *_args: Any, **_kwargs: Any) -> Any:
    return arg


def tensor(*_args: Any, **_kwargs: Any) -> Tensor:
    return Tensor(*_args, **_kwargs)


def randn(*_args: Any, **_kwargs: Any) -> Tensor:
    return Tensor(*_args, **_kwargs)


def randint(*_args: Any, **_kwargs: Any) -> Tensor:
    return Tensor(*_args, **_kwargs)


def relu(x: Any) -> Any:
    return x


def set_float32_matmul_precision(*_args: Any, **_kwargs: Any) -> None:
    return None


def manual_seed(*_args: Any, **_kwargs: Any) -> int:
    return 0


def save(*_args: Any, **_kwargs: Any) -> None:
    return None


def load(*_args: Any, **_kwargs: Any) -> Any:
    return None


float32 = _DType("float32")
float64 = _DType("float64")
float16 = _DType("float16")
float = float32
double = float64
bfloat = _DType("bfloat")
bfloat16 = _DType("bfloat16")
half = float16
int8 = _DType("int8")
uint8 = _DType("uint8")
int64 = _DType("int64")
int32 = _DType("int32")
long = int64
int = int32
bool = _DType("bool")


nn = _register_module("torch.nn", _make_module("torch.nn"))


class Module:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__()

    def parameters(self):
        return []

    def to(self, *_args: Any, **_kwargs: Any) -> "Module":
        return self

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.forward(*args, **kwargs)  # type: ignore[attr-defined]


class Linear(Module):
    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        super().__init__()

    def forward(self, x: Any) -> Any:
        return x


class Parameter(Tensor):
    pass


nn.Module = Module
nn.Linear = Linear
nn.Parameter = Parameter

nn_modules = _register_module("torch.nn.modules", _make_module("torch.nn.modules"))
nn.modules = nn_modules

nn_modules_module = _register_module("torch.nn.modules.module", _make_module("torch.nn.modules.module"))


class _IncompatibleKeys(tuple):
    pass


nn_modules_module._IncompatibleKeys = _IncompatibleKeys
nn_modules.module = nn_modules_module

functional = _register_module("torch.nn.functional", _make_module("torch.nn.functional"))
functional.relu = relu
functional.cross_entropy = _return_first
nn.functional = functional

nn_utils = _register_module("torch.nn.utils", _make_module("torch.nn.utils"))
nn.utils = nn_utils

prune = _register_module("torch.nn.utils.prune", _make_module("torch.nn.utils.prune"))


class BasePruningMethod:
    pass


class LnStructured(BasePruningMethod):
    pass


class L1Unstructured(BasePruningMethod):
    pass


class RandomStructured(BasePruningMethod):
    pass


class RandomUnstructured(BasePruningMethod):
    pass


for _name in [
    "BasePruningMethod",
    "LnStructured",
    "L1Unstructured",
    "RandomStructured",
    "RandomUnstructured",
]:
    setattr(prune, _name, globals()[_name])

for _name in [
    "custom_from_mask",
    "global_unstructured",
    "identity",
    "ln_structured",
    "l1_unstructured",
    "random_structured",
    "random_unstructured",
]:
    setattr(prune, _name, _noop)


optim = _register_module("torch.optim", _make_module("torch.optim"))


class Optimizer:
    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        pass

    def step(self) -> None:
        return None

    def zero_grad(self) -> None:
        return None


class Adam(Optimizer):
    pass


optim.Optimizer = Optimizer
optim.Adam = Adam

lr_scheduler = _register_module("torch.optim.lr_scheduler", _make_module("torch.optim.lr_scheduler"))


class LRScheduler:
    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        pass


class ReduceLROnPlateau(LRScheduler):
    pass


lr_scheduler.LRScheduler = LRScheduler
lr_scheduler.ReduceLROnPlateau = ReduceLROnPlateau
optim.lr_scheduler = lr_scheduler


cuda = _register_module("torch.cuda", _make_module("torch.cuda"))
cuda.is_available = lambda: False
cuda.device_count = lambda: 0
cuda.set_device = _noop
cuda.memory_stats = lambda *_args, **_kwargs: {}
cuda.empty_cache = _noop
cuda.current_device = lambda: 0


distributed = _register_module("torch.distributed", _make_module("torch.distributed"))
distributed.is_available = lambda: False
distributed.is_initialized = lambda: False
distributed.get_rank = lambda: 0
distributed.get_world_size = lambda: 1
distributed.barrier = _noop
distributed.init_process_group = _noop


multiprocessing = _register_module("torch.multiprocessing", _make_module("torch.multiprocessing"))
multiprocessing.get_all_start_methods = lambda: ["spawn"]


utils = _register_module("torch.utils", _make_module("torch.utils"))
data = _register_module("torch.utils.data", _make_module("torch.utils.data"))


class Dataset:
    pass


class Sampler:
    def __iter__(self):
        return iter(())

    def __len__(self) -> int:
        return 0


class BatchSampler(Sampler):
    pass


class RandomSampler(Sampler):
    pass


class SequentialSampler(Sampler):
    pass


class TensorDataset(Dataset):
    def __init__(self, *tensors: Tensor) -> None:
        self.tensors = tensors


class DistributedSampler(Sampler):
    def __init__(self, dataset: Dataset, *args: Any, **kwargs: Any) -> None:
        self.dataset = dataset

    def __iter__(self):
        return iter(())


class DataLoader:
    def __init__(self, dataset: Dataset, *args: Any, **kwargs: Any) -> None:
        self.dataset = dataset

    def __iter__(self):
        return iter(())


data.Dataset = Dataset
data.Sampler = Sampler
data.BatchSampler = BatchSampler
data.RandomSampler = RandomSampler
data.SequentialSampler = SequentialSampler
data.TensorDataset = TensorDataset
data.DistributedSampler = DistributedSampler
data.DataLoader = DataLoader
utils.data = data

data_distributed = _register_module("torch.utils.data.distributed", _make_module("torch.utils.data.distributed"))
data_distributed.DistributedSampler = DistributedSampler
data.distributed = data_distributed


backends = _register_module("torch.backends", _make_module("torch.backends"))
mps = _register_module("torch.backends.mps", _make_module("torch.backends.mps"))
mps.is_available = lambda: False
backends.mps = mps


version = _register_module("torch.version", _make_module("torch.version"))
version.hip = None


class _CModule:
    _GLIBCXX_USE_CXX11_ABI = 0


_C = _CModule()


class _Ops:
    pass


ops = _Ops()


def __getattr__(name: str) -> Any:
    placeholder = types.SimpleNamespace(__name__=f"torch.{name}")
    return placeholder

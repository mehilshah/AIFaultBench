#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import logging
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "codebase" / "torchtitan" / "components" / "dataloader.py"


def install_stubs() -> None:
    """Install minimal import stubs so we can load the real source file.

    The host environment has a broken torch install, so the repro avoids any
    third-party dependency by stubbing the imports that dataloader.py expects.
    """

    for name in [
        "torchtitan",
        "torchtitan.tools",
        "torchtitan.tools.logging",
        "torch",
        "torch.distributed",
        "torch.distributed.checkpoint",
        "torch.distributed.checkpoint.stateful",
        "torch.utils",
        "torch.utils.data",
        "torchdata",
        "torchdata.stateful_dataloader",
    ]:
        sys.modules.pop(name, None)

    torchtitan_pkg = types.ModuleType("torchtitan")
    torchtitan_pkg.__path__ = []
    sys.modules["torchtitan"] = torchtitan_pkg

    torchtitan_tools_pkg = types.ModuleType("torchtitan.tools")
    torchtitan_tools_pkg.__path__ = []
    sys.modules["torchtitan.tools"] = torchtitan_tools_pkg

    logging_mod = types.ModuleType("torchtitan.tools.logging")
    logging_mod.logger = logging.getLogger("torchtitan-repro")
    sys.modules["torchtitan.tools.logging"] = logging_mod

    for pkg_name in [
        "torch",
        "torch.distributed",
        "torch.distributed.checkpoint",
        "torch.utils",
        "torchdata",
    ]:
        pkg = types.ModuleType(pkg_name)
        pkg.__path__ = []
        sys.modules[pkg_name] = pkg

    stateful_mod = types.ModuleType("torch.distributed.checkpoint.stateful")

    class Stateful:
        pass

    stateful_mod.Stateful = Stateful
    sys.modules["torch.distributed.checkpoint.stateful"] = stateful_mod

    data_mod = types.ModuleType("torch.utils.data")

    class IterableDataset:
        pass

    data_mod.IterableDataset = IterableDataset
    sys.modules["torch.utils.data"] = data_mod

    sd_mod = types.ModuleType("torchdata.stateful_dataloader")

    class StatefulDataLoader:
        def __init__(self, *args, **kwargs):
            pass

    sd_mod.StatefulDataLoader = StatefulDataLoader
    sys.modules["torchdata.stateful_dataloader"] = sd_mod


def load_target_module():
    install_stubs()
    spec = importlib.util.spec_from_file_location("dataloader_under_test", TARGET)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {TARGET}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def batch_generator(stop_exc, data_iterable):
    data_iterator = iter(data_iterable)
    while True:
        try:
            batch = next(data_iterator)
        except StopIteration as ex:
            # This mirrors torchtitan/train.py and torchtitan/components/dataloader.py.
            raise stop_exc() from ex
        yield batch


def main() -> int:
    module = load_target_module()

    print(f"Loaded: {TARGET.relative_to(ROOT)}")
    print(
        "DataloaderStopIteration is subclass of StopIteration:",
        issubclass(module.DataloaderStopIteration, StopIteration),
    )
    print("Starting data consumption loop...")

    dataiter = batch_generator(module.DataloaderStopIteration, [])
    try:
        next(dataiter)
        print("UNEXPECTED: batch was produced")
        return 2
    except module.DataloaderStopIteration:
        print("Gracefully handled the end of data.")
        return 0
    except Exception as exc:
        print(f"Caught unexpected exception: {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

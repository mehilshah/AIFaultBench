#!/usr/bin/env python3
"""Reproduce the DELF packaging bug from the local source tree.

The source tree contains the `delf/python/datasets/` files, but the package is
missing an `__init__.py`. `setup.py` uses `find_packages()`, so an installed
distribution omits that package and importing `delf` fails later when
`delf/__init__.py` reaches `from delf.python.datasets import ...`.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "codebase" / "research" / "delf"
RESULT_PATH = ROOT / "reproduction.json"


def _run(cmd, *, env=None, cwd=None):
    return subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _sitecustomize_source() -> str:
    return textwrap.dedent(
        r'''
        import sys
        import types

        class _Proxy:
            def __init__(self, name):
                self._name = name

            def __call__(self, *args, **kwargs):
                if self._name == "tensorflow.function":
                    if args and callable(args[0]) and len(args) == 1 and not kwargs:
                        return args[0]
                    return lambda fn: fn
                return _Proxy(self._name + "()")

            def __getattr__(self, item):
                return _Proxy(f"{self._name}.{item}")

            def __iter__(self):
                return iter(())

            def __bool__(self):
                return False

            def __repr__(self):
                return f"<proxy {self._name}>"


        class _DummyBase:
            def __init__(self, *args, **kwargs):
                pass

            def __call__(self, *args, **kwargs):
                return _Proxy(self.__class__.__name__)

            @classmethod
            def from_config(cls, *args, **kwargs):
                return cls()


        def _dummy_class(name):
            return type(name.rsplit(".", 1)[-1], (_DummyBase,), {})


        def _module(name, attrs=None):
            mod = types.ModuleType(name)
            mod.__dict__["__package__"] = name.rpartition(".")[0]
            mod.__dict__["__path__"] = []

            def __getattr__(attr):
                return _Proxy(f"{name}.{attr}")

            mod.__getattr__ = __getattr__  # type: ignore[attr-defined]
            if attrs:
                mod.__dict__.update(attrs)
            sys.modules[name] = mod
            return mod


        # Basic scientific stack stubs.
        _module("numpy")
        _module("pandas")
        _module("scipy")
        _module("scipy.io")
        _module("scipy.io.matlab", {"loadmat": lambda *a, **k: {}})

        # absl stubs used by training/build_image_dataset.py.
        flags_ns = types.SimpleNamespace(
            FLAGS=types.SimpleNamespace(),
            DEFINE_string=lambda *a, **k: None,
            DEFINE_integer=lambda *a, **k: None,
            DEFINE_float=lambda *a, **k: None,
            DEFINE_boolean=lambda *a, **k: None,
            DEFINE_bool=lambda *a, **k: None,
        )
        app_ns = types.SimpleNamespace(run=lambda *a, **k: None)
        logging_ns = types.SimpleNamespace(
            info=lambda *a, **k: None,
            warning=lambda *a, **k: None,
            error=lambda *a, **k: None,
            debug=lambda *a, **k: None,
        )
        _module("absl", {"app": app_ns, "flags": flags_ns, "logging": logging_ns})
        sys.modules["absl.app"] = app_ns  # type: ignore[assignment]
        sys.modules["absl.flags"] = flags_ns  # type: ignore[assignment]
        sys.modules["absl.logging"] = logging_ns  # type: ignore[assignment]

        # h5py is imported during model package initialization.
        _module("h5py")

        # protobuf and object_detection are needed at import time.
        _module("google")
        _module("google.protobuf")
        _module("google.protobuf.text_format", {"Merge": lambda *a, **k: None})

        _module("object_detection")
        _module("object_detection.core")
        _module("object_detection.core.box_list")
        _module("object_detection.core.box_list_ops")

        # TensorFlow is only needed as a structural import target here.
        keras_layers = _module(
            "tensorflow.keras.layers",
            {"Layer": _DummyBase, "Model": _DummyBase},
        )

        def _keras_layers_getattr(attr):
            if attr in {"Layer", "Model"}:
                return _DummyBase
            cls = _dummy_class(f"tensorflow.keras.layers.{attr}")
            setattr(keras_layers, attr, cls)
            return cls

        keras_layers.__getattr__ = _keras_layers_getattr  # type: ignore[attr-defined]

        keras_mod = _module(
            "tensorflow.keras",
            {
                "Model": _DummyBase,
                "Sequential": _DummyBase,
                "layers": keras_layers,
                "regularizers": _Proxy("tensorflow.keras.regularizers"),
                "activations": _Proxy("tensorflow.keras.activations"),
                "optimizers": _Proxy("tensorflow.keras.optimizers"),
                "losses": _Proxy("tensorflow.keras.losses"),
                "metrics": _Proxy("tensorflow.keras.metrics"),
                "callbacks": _Proxy("tensorflow.keras.callbacks"),
                "applications": _Proxy("tensorflow.keras.applications"),
                "utils": _Proxy("tensorflow.keras.utils"),
                "initializers": _Proxy("tensorflow.keras.initializers"),
            },
        )

        def _keras_getattr(attr):
            if attr in keras_mod.__dict__:
                return keras_mod.__dict__[attr]
            proxy = _Proxy(f"tensorflow.keras.{attr}")
            setattr(keras_mod, attr, proxy)
            return proxy

        keras_mod.__getattr__ = _keras_getattr  # type: ignore[attr-defined]

        tf_ns = _module(
            "tensorflow",
            {
                "function": lambda fn=None, **kwargs: (
                    fn if (fn is not None and callable(fn)) else (lambda wrapped: wrapped)
                ),
                "saved_model": types.SimpleNamespace(
                    load=lambda *a, **k: _Proxy("tensorflow.saved_model.load"),
                    save=lambda *a, **k: None,
                ),
                "io": types.SimpleNamespace(
                    gfile=types.SimpleNamespace(
                        GFile=lambda *a, **k: None,
                        exists=lambda *a, **k: False,
                        makedirs=lambda *a, **k: None,
                        glob=lambda *a, **k: [],
                        copy=lambda *a, **k: None,
                        remove=lambda *a, **k: None,
                    ),
                    parse_single_example=lambda *a, **k: {},
                    decode_jpeg=lambda *a, **k: None,
                    TFRecordWriter=lambda *a, **k: None,
                    FixedLenFeature=lambda *a, **k: None,
                ),
                "train": types.SimpleNamespace(
                    Checkpoint=lambda *a, **k: types.SimpleNamespace(
                        restore=lambda *a, **k: None
                    ),
                    CheckpointManager=lambda *a, **k: None,
                ),
                "keras": keras_mod,
                "compat": types.SimpleNamespace(v1=_Proxy("tensorflow.compat.v1")),
                "math": _Proxy("tensorflow.math"),
                "nn": _Proxy("tensorflow.nn"),
                "image": _Proxy("tensorflow.image"),
                "dtypes": types.SimpleNamespace(cast=lambda *a, **k: None),
                "cast": lambda *a, **k: None,
                "constant": lambda *a, **k: None,
                "convert_to_tensor": lambda *a, **k: None,
                "range": lambda *a, **k: [],
                "reshape": lambda *a, **k: None,
                "expand_dims": lambda *a, **k: None,
                "squeeze": lambda *a, **k: None,
                "shape": lambda *a, **k: [],
                "zeros": lambda *a, **k: None,
                "ones_like": lambda *a, **k: None,
                "where": lambda *a, **k: [],
                "gather": lambda *a, **k: None,
                "concat": lambda *a, **k: None,
                "divide": lambda *a, **k: None,
                "matmul": lambda *a, **k: None,
                "slice": lambda *a, **k: None,
                "sqrt": lambda *a, **k: None,
                "reduce_sum": lambda *a, **k: None,
                "minimum": lambda *a, **k: None,
                "round": lambda *a, **k: None,
                "less": lambda *a, **k: None,
                "nest": types.SimpleNamespace(map_structure=lambda *a, **k: None),
                "stop_gradient": lambda *a, **k: None,
                "Variable": lambda *a, **k: None,
                "zeros_like": lambda *a, **k: None,
            },
        )
        tf_ns.__dict__["float32"] = object()
        tf_ns.__dict__["int32"] = object()
        tf_ns.__dict__["string"] = object()

        # delf's generated protobufs are absent from the source checkout; keep
        # the import chain moving so we can reach the real datasets failure.
        aggregation_constants = types.SimpleNamespace(VLAD=1, ASMK=2, ASMK_STAR=3)
        delf_protos = {
            "delf.protos.aggregation_config_pb2": types.SimpleNamespace(
                AggregationConfig=aggregation_constants
            ),
            "delf.protos.box_pb2": types.SimpleNamespace(Boxes=type("Boxes", (), {})),
            "delf.protos.datum_pb2": types.SimpleNamespace(
                DatumProto=type("DatumProto", (), {}),
                DatumPairProto=type("DatumPairProto", (), {}),
            ),
            "delf.protos.delf_config_pb2": types.SimpleNamespace(
                DelfConfig=type("DelfConfig", (), {})
            ),
            "delf.protos.feature_pb2": types.SimpleNamespace(
                DelfFeatures=type("DelfFeatures", (), {})
            ),
        }
        for name, module in delf_protos.items():
            sys.modules[name] = module
        '''
    ).lstrip()


def main() -> int:
    print(f"source tree: {SOURCE}")
    print("checking package discovery...")
    pkg_check = _run(
        [
            sys.executable,
            "-c",
            "from setuptools import find_packages; "
            "pkgs = find_packages('codebase/research/delf'); "
            "print('delf.python.datasets' in pkgs); "
            "print(pkgs)",
        ],
        cwd=ROOT,
    )
    print(pkg_check.stdout.rstrip())
    if pkg_check.returncode != 0:
        print(pkg_check.stderr.rstrip(), file=sys.stderr)

    with tempfile.TemporaryDirectory(prefix="delf-repro-") as tmp:
        tmp = Path(tmp)
        site_dir = tmp / "site"
        stub_dir = tmp / "stubs"
        site_dir.mkdir()
        stub_dir.mkdir()

        print("installing the package without extra deps...")
        install = _run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--no-deps",
                "--target",
                str(site_dir),
                str(SOURCE),
            ],
            cwd=ROOT,
            env={**os.environ, "PIP_DISABLE_PIP_VERSION_CHECK": "1"},
        )
        print(install.stdout.rstrip())
        if install.returncode != 0:
            print(install.stderr.rstrip(), file=sys.stderr)
            write_result(
                reproducible=False,
                evidence="package install failed before the import path was reached",
                steps=[
                    "Build and install the DELF package into a temporary site directory.",
                ],
                blocking_reason="temporary install failed",
                reproduction_command="bash run_repro.sh",
            )
            return 1

        _write(stub_dir / "sitecustomize.py", _sitecustomize_source())

        cmd = [
            sys.executable,
            "-c",
            "import delf",
        ]
        env = {
            **os.environ,
            "PYTHONPATH": str(stub_dir) + os.pathsep + str(site_dir),
            "PYTHONNOUSERSITE": "1",
        }
        print("running import reproduction...")
        proc = _run(cmd, env=env, cwd=ROOT)
        if proc.stdout:
            print(proc.stdout.rstrip())
        if proc.stderr:
            print(proc.stderr.rstrip(), file=sys.stderr)

        missing = "ModuleNotFoundError: No module named 'delf.python.datasets'"
        reproducible = proc.returncode != 0 and missing in (proc.stderr or "")
        evidence = (
            "importing the installed delf package fails with the expected "
            "ModuleNotFoundError"
            if reproducible
            else "the observed failure did not match the reported datasets import error"
        )
        blocking_reason = "" if reproducible else "import failed for a different reason"
        steps = [
            "Install the DELF source tree from codebase/research/delf without extra dependencies.",
            "Import delf from the installed package using a stubbed runtime for TensorFlow and other unrelated libraries.",
            "Observe that delf/__init__.py eventually imports delf.python.datasets and fails because that package is not present in the built distribution.",
        ]
        write_result(
            reproducible=reproducible,
            evidence=evidence,
            steps=steps,
            blocking_reason=blocking_reason,
            reproduction_command="bash run_repro.sh",
        )

        print(json.dumps({
            "reproducible": reproducible,
            "evidence": evidence,
        }, indent=2))
        return 0 if reproducible else 1


def write_result(*, reproducible, evidence, steps, blocking_reason, reproduction_command):
    payload = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": reproduction_command,
    }
    RESULT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())

"""Import helper for the bundled source-less cpython-311 snapshot.

The standardized folder only contains `.pyc` files for the upstream codebase.
This helper installs a meta path finder that can import those modules directly
from `codebase/` while auto-linking child modules onto their parent packages.
"""

from __future__ import annotations

import importlib.abc
import importlib.machinery
import importlib.util
import sys
import types
from pathlib import Path


STUB_PACKAGES = [
    "official",
    "official.common",
    "official.core",
    "official.modeling",
    "official.vision",
    "official.vision.configs",
    "official.vision.tasks",
    "official.vision.modeling",
    "official.vision.modeling.backbones",
    "official.vision.modeling.layers",
    "official.vision.modeling.heads",
    "official.vision.modeling.decoders",
]


class _LinkLoader(importlib.abc.Loader):
    def __init__(self, fullname: str, path: str, is_pkg: bool):
        self._fullname = fullname
        self._path = path
        self._is_pkg = is_pkg
        self._inner = importlib.machinery.SourcelessFileLoader(fullname, path)

    def create_module(self, spec):  # type: ignore[override]
        return None

    def exec_module(self, module):  # type: ignore[override]
        module.__file__ = self._path
        module.__loader__ = self
        module.__package__ = self._fullname if self._is_pkg else self._fullname.rpartition(".")[0]
        if self._is_pkg:
            module.__path__ = [str(Path(self._path).parents[1])]
        self._inner.exec_module(module)

        parent, _, child = self._fullname.rpartition(".")
        if parent and parent in sys.modules:
            setattr(sys.modules[parent], child, module)


class _PycFinder(importlib.abc.MetaPathFinder):
    def __init__(self, root: Path):
        self._root = root

    def find_spec(self, fullname, path=None, target=None):  # type: ignore[override]
        parts = fullname.split(".")
        base = self._root.joinpath(*parts)
        pkg_pyc = base / "__pycache__" / "__init__.cpython-311.pyc"
        mod_pyc = base.parent / "__pycache__" / f"{parts[-1]}.cpython-311.pyc"

        if pkg_pyc.exists() and fullname not in sys.modules:
            loader = _LinkLoader(fullname, str(pkg_pyc), True)
            spec = importlib.util.spec_from_loader(fullname, loader, is_package=True)
            spec.submodule_search_locations = [str(base)]
            return spec

        if mod_pyc.exists():
            loader = _LinkLoader(fullname, str(mod_pyc), False)
            return importlib.util.spec_from_loader(fullname, loader, is_package=False)

        return None


def install(root: str | Path | None = None) -> Path:
    """Install the loader and seed package stubs.

    Returns the resolved root path for convenience.
    """

    root_path = Path(root or Path(__file__).resolve().parent / "codebase").resolve()
    for pkg in STUB_PACKAGES:
        if pkg not in sys.modules:
            module = types.ModuleType(pkg)
            module.__path__ = [str(root_path.joinpath(*pkg.split(".")))]
            sys.modules[pkg] = module

    if not any(isinstance(f, _PycFinder) for f in sys.meta_path):
        sys.meta_path.insert(0, _PycFinder(root_path))

    return root_path


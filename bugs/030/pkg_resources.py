"""Minimal compatibility shim for older PyTorch Lightning imports.

Lightning 1.7.x expects a subset of the legacy ``pkg_resources`` API that is
no longer present in newer setuptools releases. The repro only needs version
lookups and namespace declaration, so this shim keeps the bundle runnable
without mutating the code under test.
"""

from __future__ import annotations

import importlib.metadata as importlib_metadata
import re
from dataclasses import dataclass

from packaging.requirements import Requirement
from packaging.version import Version


class DistributionNotFound(Exception):
    pass


@dataclass
class _Distribution:
    version: str


def _normalize_requirement(requirement: str) -> str:
    # Lightning 1.7.7 occasionally passes malformed specifiers like ``1.9.*``.
    return re.sub(r"(?<=\d)\.\*", "", requirement)


def get_distribution(name: str) -> _Distribution:
    try:
        return _Distribution(importlib_metadata.version(name))
    except importlib_metadata.PackageNotFoundError as exc:
        raise DistributionNotFound(str(exc)) from exc


def require(requirements):
    if isinstance(requirements, str):
        requirements = [requirements]

    for requirement in requirements:
        parsed = Requirement(_normalize_requirement(requirement))
        try:
            installed = Version(importlib_metadata.version(parsed.name))
        except importlib_metadata.PackageNotFoundError as exc:
            raise DistributionNotFound(str(exc)) from exc
        if parsed.specifier and installed not in parsed.specifier:
            raise DistributionNotFound(
                f"{parsed.name} {installed} does not satisfy {parsed.specifier}"
            )


def declare_namespace(name: str) -> None:
    return None

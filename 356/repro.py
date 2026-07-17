#!/usr/bin/env python3
"""Reproduce or falsify the reported InverseWishart export bug."""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import types


ROOT = pathlib.Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
NUMPYRO_ROOT = CODEBASE / "numpyro"


def load_distributions_module():
    """Load ``numpyro.distributions`` without executing ``numpyro.__init__``.

    The checked-out tree imports a newer JAX API from ``numpyro.__init__`` that is
    unrelated to the bug report. Stubbing the parent package keeps the repro focused
    on the distributions namespace itself.
    """

    numpyro_pkg = types.ModuleType("numpyro")
    numpyro_pkg.__path__ = [str(NUMPYRO_ROOT)]
    sys.modules["numpyro"] = numpyro_pkg

    dist_init = NUMPYRO_ROOT / "distributions" / "__init__.py"
    spec = importlib.util.spec_from_file_location(
        "numpyro.distributions",
        dist_init,
        submodule_search_locations=[str(NUMPYRO_ROOT / "distributions")],
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not create import spec for numpyro.distributions")

    module = importlib.util.module_from_spec(spec)
    sys.modules["numpyro.distributions"] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_distributions_module()
    has_inverse_wishart = hasattr(module, "InverseWishart")
    print(f"module={module.__name__}")
    print(f"InverseWishart_present={has_inverse_wishart}")
    if has_inverse_wishart:
        print(f"InverseWishart_obj={module.InverseWishart!r}")
        return 0
    print("InverseWishart is missing from numpyro.distributions")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

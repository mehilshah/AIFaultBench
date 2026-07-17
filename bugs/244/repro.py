from __future__ import annotations

import importlib.metadata as metadata
import platform
import sys
import traceback


def has_distribution(name: str) -> bool:
    try:
        metadata.distribution(name)
    except metadata.PackageNotFoundError:
        return False
    return True


def main() -> None:
    print(f"python={sys.version.split()[0]}")
    print(f"platform={platform.platform()}")
    print(f"typing_extensions_installed={has_distribution('typing_extensions')}")
    print(f"jax_installed={has_distribution('jax')}")
    print(f"jaxlib_installed={has_distribution('jaxlib')}")

    try:
        import numpyro  # noqa: F401
    except Exception:
        traceback.print_exc()
        raise

    raise SystemExit(
        "Unexpected success: importing numpyro should fail when typing_extensions "
        "is absent."
    )


if __name__ == "__main__":
    main()

import importlib.metadata as metadata
import traceback


def main() -> None:
    print("numpyro_repro: starting")
    for pkg in ("jax", "jaxlib", "numpyro"):
        try:
            print(f"{pkg}=={metadata.version(pkg)}")
        except metadata.PackageNotFoundError:
            print(f"{pkg}: not installed")

    try:
        import numpyro  # noqa: F401
    except Exception:
        print("numpyro import failed:")
        traceback.print_exc()
        raise

    print("numpyro import succeeded")


if __name__ == "__main__":
    main()

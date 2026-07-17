import warnings


warnings.simplefilter("error", DeprecationWarning)

print("Importing timm with DeprecationWarnings treated as errors...", flush=True)
import timm  # noqa: F401

print("Imported timm successfully", flush=True)

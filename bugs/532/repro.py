#!/usr/bin/env python3
import os
import sys


ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "codebase", "src"))

from diffusers import ErnieImageTransformer2DModel


print("has_from_single_file:", hasattr(ErnieImageTransformer2DModel, "from_single_file"))

# This is the public API the bug report references.
ErnieImageTransformer2DModel.from_single_file(
    "path/to/transformer.safetensors",
    config="path/to/base_model",
    subfolder="transformer",
)

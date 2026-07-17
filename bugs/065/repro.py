#!/usr/bin/env python3
"""Minimal reproduction for the FeatureSpace import failure."""

print("Reproducing: from keras.utils import FeatureSpace")
from keras.utils import FeatureSpace  # noqa: F401

print("Imported FeatureSpace successfully")

#!/usr/bin/env python3
"""Reproduce the TensorFlow-import-first JAX NCCL collective bug."""

from __future__ import annotations

import argparse
import os
import platform
import sys
import traceback


def _print_header(import_tensorflow: bool) -> None:
  print("=== repro context ===")
  print(f"python: {sys.version.split()[0]}")
  print(f"platform: {platform.platform()}")
  print(f"cwd: {os.getcwd()}")
  print(f"import_tensorflow: {import_tensorflow}")


def _run_collective(import_tensorflow: bool) -> int:
  if import_tensorflow:
    import tensorflow as tf  # noqa: F401

    print(f"tensorflow: {tf.__version__}")

  import jax
  import jax.numpy as jnp
  from jax.sharding import Mesh, NamedSharding, PartitionSpec as P

  print(f"jax: {jax.__version__}")
  devices = list(jax.devices())
  gpu_devices = [d for d in devices if getattr(d, "platform", "") == "gpu"]
  print(f"jax.devices(): {devices}")
  print(f"gpu devices: {gpu_devices}")

  if len(gpu_devices) < 2:
    print(
        "BLOCKED: this repro needs at least two local GPU devices to exercise "
        "the NCCL collective path from the bug report.",
        file=sys.stderr,
    )
    return 2

  mesh = Mesh(gpu_devices[:2], ("d",))
  x = jax.device_put(
      jnp.ones((8, 128), jnp.float16),
      NamedSharding(mesh, P("d", None)),
  )
  fn = jax.jit(
      lambda a: a.sum(),
      out_shardings=NamedSharding(mesh, P()),
  )

  try:
    result = fn(x)
    print(f"result: {result}")
    return 0
  except Exception:
    traceback.print_exc()
    return 1


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
      "--with-tensorflow",
      action="store_true",
      help="Import TensorFlow before the JAX collective.",
  )
  args = parser.parse_args()

  _print_header(args.with_tensorflow)
  return _run_collective(args.with_tensorflow)


if __name__ == "__main__":
  raise SystemExit(main())

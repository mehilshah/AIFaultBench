from __future__ import annotations

import os
import sys


ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "codebase"))

import jax

jax.config.update("jax_num_cpu_devices", 2)

import jax.numpy as jnp
from jax import random
from jax.sharding import Mesh, NamedSharding, PartitionSpec as P


trace_count = 0


@jax.jit
def jitted_identity(x):
  global trace_count
  trace_count += 1
  return x


def sharded_key():
  mesh = Mesh(jax.devices(), ("a",))
  return jax.device_put(random.key(0), NamedSharding(mesh, P()))


def unsharded_key():
  return random.key(0)


def single_device_key():
  mesh = Mesh(jax.devices()[:1], ("a",))
  return jax.device_put(random.key(0), NamedSharding(mesh, P()))


def sharded_float():
  mesh = Mesh(jax.devices(), ("a",))
  return jax.device_put(jnp.zeros(()), NamedSharding(mesh, P()))


def run(fresh_value, n_iters, feed_output_back=True):
  global trace_count
  trace_count = 0
  x = fresh_value()
  cache_sizes = []
  for i in range(n_iters):
    out = jitted_identity(x)
    if feed_output_back:
      x = out
    cache_size = jitted_identity._cache_size()
    cache_sizes.append(cache_size)
    print(f"  i={i}: cpp cache size = {cache_size}, traces = {trace_count}")
  return cache_sizes


def demo(fresh_value, feed_output_back=True):
  jitted_identity.clear_cache()
  runs = []
  for call in range(2):
    print(f"run {call + 1}:")
    runs.append(run(fresh_value, 3, feed_output_back))
  return runs


def main():
  print("devices:", jax.devices())

  print()
  print("part 1: spurious second cache entry on the 3rd invocation")
  runs = demo(sharded_key)
  if runs[0] != [1, 1, 2] or runs[1] != [2, 2, 2]:
    raise AssertionError(f"unexpected cache sizes for sharded_key: {runs}")

  print()
  print("negative controls: no spurious entry, cache sizes all 1")
  for fresh_value in (unsharded_key, single_device_key, sharded_float):
    print(f"\n{fresh_value.__name__}:")
    runs = demo(fresh_value)
    if runs != [[1, 1, 1], [1, 1, 1]]:
      raise AssertionError(f"unexpected control result for {fresh_value.__name__}: {runs}")

  print("\nsharded_key, same fresh key every call (no feedback):")
  runs = demo(sharded_key, feed_output_back=False)
  if runs != [[1, 1, 1], [1, 1, 1]]:
    raise AssertionError(f"unexpected no-feedback result: {runs}")

  print()
  print("part 2: no_tracing catches the extra dispatch (2 invocations per run)")
  jitted_identity.clear_cache()
  run(sharded_key, 2)
  try:
    with jax.no_tracing():
      run(sharded_key, 2)
  except RuntimeError as e:
    print("RAISED:", e)
  else:
    raise AssertionError("expected jax.no_tracing to raise on the fastpath-produced key")

  print()
  print("part 3: workaround: pass raw key data across the jit boundary")

  @jax.jit
  def jitted_identity_on_data(data):
    key = random.wrap_key_data(data)
    return random.key_data(key)

  def sharded_key_data():
    mesh = Mesh(jax.devices(), ("a",))
    return jax.device_put(random.key_data(random.key(0)), NamedSharding(mesh, P()))

  x = sharded_key_data()
  cache_sizes = []
  for i in range(4):
    x = jitted_identity_on_data(x)
    cache_size = jitted_identity_on_data._cache_size()
    cache_sizes.append(cache_size)
    print(f"  i={i}: cpp cache size = {cache_size}")
  if cache_sizes != [1, 1, 1, 1]:
    raise AssertionError(f"unexpected workaround result: {cache_sizes}")

  print()
  print("REPRODUCED: sharded PRNG key outputs create a second C++ fastpath cache entry.")


if __name__ == "__main__":
  main()

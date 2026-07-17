import gc
import os
import subprocess
import sys


os.environ.setdefault("XLA_PYTHON_CLIENT_ALLOCATOR", "platform")

import jax
import jax.numpy as jnp


def gpu_used_mib(pid: int) -> int:
  out = subprocess.check_output(
      [
          "nvidia-smi",
          "--query-compute-apps=pid,used_memory",
          "--format=csv,noheader,nounits",
      ],
      text=True,
  )
  for line in out.splitlines():
    parts = [part.strip() for part in line.split(",")]
    if len(parts) >= 2 and parts[0] == str(pid):
      return int(parts[1])
  raise RuntimeError(f"PID {pid} was not listed by nvidia-smi")


def report(tag: str, pid: int, baseline: int) -> int:
  used = gpu_used_mib(pid)
  print(
      f"{tag:32s} pid={pid} gpu_used={used} MiB "
      f"(delta={used - baseline:+d} MiB)"
  )
  return used


def main() -> int:
  pid = os.getpid()
  print("jax", jax.__version__)
  print("devices", jax.devices())

  baseline = gpu_used_mib(pid)
  print(f"baseline                         pid={pid} gpu_used={baseline} MiB")

  # Scale the original issue report down so this bundle fits on a busy GPU.
  x = jnp.ones((8, 1024, 1024, 32), dtype=jnp.float32)
  x.block_until_ready()
  after_alloc = report("1 GiB array allocated", pid, baseline)
  del x
  gc.collect()
  after_free = report("after del + gc", pid, baseline)

  @jax.jit
  def batched_gram_norm(a):
    return jax.vmap(lambda row: row @ row.T)(a).sum()

  n, k = 1024, 8
  for batch in (192, 320, 256):
    a = jnp.ones((batch, n, k), dtype=jnp.float32)
    batched_gram_norm(a).block_until_ready()
    del a
    gc.collect()
    scratch_gib = batch * n * n * 4 / 2**30
    report(f"after vmap call ({scratch_gib:.1f} GiB scratch)", pid, baseline)

  final = report("final (nothing live)", pid, baseline)

  if after_free - baseline < 500:
    raise AssertionError(
        f"Expected platform allocator to retain at least 500 MiB after free; "
        f"got {after_free - baseline} MiB"
    )
  if final - baseline < 1000:
    raise AssertionError(
        f"Expected platform allocator to retain at least 1 GiB at the end; "
        f"got {final - baseline} MiB"
    )

  return 0


if __name__ == "__main__":
  sys.exit(main())

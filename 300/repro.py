#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile
from pathlib import Path


MODEL_ID = "google/ddpm-cifar10-32"


def run_phase(cache_dir: str, offline: bool) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["HF_HOME"] = cache_dir
    if offline:
        env["HF_HUB_OFFLINE"] = "1"
    else:
        env.pop("HF_HUB_OFFLINE", None)

    snippet = f"""
from diffusers import DiffusionPipeline
path = DiffusionPipeline.download(
    {MODEL_ID!r},
    cache_dir={cache_dir!r},
)
print(path)
"""
    return subprocess.run(
        [sys.executable, "-c", snippet],
        env=env,
        text=True,
        capture_output=True,
    )


def main() -> int:
    cache_dir = tempfile.mkdtemp(prefix="repro-hf-cache-")
    print(f"cache_dir={cache_dir}")
    print(f"model_id={MODEL_ID}")

    online = run_phase(cache_dir, offline=False)
    sys.stdout.write(online.stdout)
    sys.stderr.write(online.stderr)
    if online.returncode != 0:
        print("RESULT: setup failure during online download")
        return online.returncode

    offline = run_phase(cache_dir, offline=True)
    sys.stdout.write(offline.stdout)
    sys.stderr.write(offline.stderr)

    if offline.returncode == 0:
        print("RESULT: not reproducible - offline reload unexpectedly succeeded")
        return 1

    stderr = offline.stderr
    if "offline mode is enabled" in stderr and "Cannot load model" in stderr:
        print("RESULT: reproducible - offline reload failed after online cache warmup")
        return 0

    print("RESULT: unexpected failure mode")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

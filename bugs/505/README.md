# Bug 505 Reproduction Bundle

This bundle reproduces the async-copy race described in `bug_report.txt`.

The report points to `vllm/v1/utils.py::CpuGpuBuffer.copy_to_gpu()` using
`non_blocking=True`, then reusing the copied tensor on a different stream
without synchronization. The minimal repro here uses the same pattern:

- a pinned CPU buffer
- an async H2D copy to CUDA
- an immediate read from a different CUDA stream
- a synchronized follow-up read that returns the expected value

Files:

- `repro.py`: minimal CUDA stream race repro
- `requirements.txt`: runtime dependencies for the repro
- `setup_env.sh`: create and populate a clean virtualenv
- `run_repro.sh`: convenience wrapper for running the repro
- `manifest.json`: bundle metadata
- `reproduction.json`: machine-readable result after running the repro

Run locally:

```bash
bash setup_env.sh
bash run_repro.sh
```

The expected failing behavior is an unsynchronized read that observes stale
data (`0`) where the CPU buffer had already been updated to `100`, followed by
a synchronized read that sees the correct value.

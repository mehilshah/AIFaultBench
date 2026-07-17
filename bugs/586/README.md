# Bug 586

This folder contains a self-contained reproduction bundle for DeepSpeed issue #7718.

What the bundle does:
- installs a CPU-capable DeepSpeed test environment from scratch
- runs a two-rank `torchrun` job
- compares one synthetic training step under DDP, ZeRO-2, and ZeRO-3
- writes the verdict to `reproduction.json`

Files:
- [`bug_report.txt`](./bug_report.txt)
- [`codebase/`](./codebase)
- [`repro.py`](./repro.py)
- [`requirements.txt`](./requirements.txt)
- [`setup_env.sh`](./setup_env.sh)
- [`run_repro.sh`](./run_repro.sh)
- [`manifest.json`](./manifest.json)
- [`reproduction.json`](./reproduction.json)
- [`repro_stdout.log`](./repro_stdout.log)
- [`repro_stderr.log`](./repro_stderr.log)

Current local result:
- not reproducible in this environment
- ZeRO-2 and ZeRO-3 both matched the DDP gradient baseline on CPU/gloo
- the GPU/stream-overlap path described in the report was not triggered here

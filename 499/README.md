# Bug 499

This folder reproduces Lightning issue 21561 in a self-contained way against the local `codebase/` tree.

What the repro does:
- installs a CPU-only PyTorch build into an isolated virtual environment
- imports Lightning from `codebase/src`
- forces `torch.cuda.is_initialized()` to return `true`
- runs `Trainer(strategy="ddp_notebook", accelerator="gpu", devices=2).fit(...)`
- captures the expected `RuntimeError` from the multiprocessing launcher guard

Run it from this folder:
```bash
bash setup_env.sh
bash run_repro.sh
```

Generated logs:
- `repro_stdout.log`
- `repro_stderr.log`

Result summary is written to `reproduction.json`.

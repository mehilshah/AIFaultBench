# Bug 527

This folder contains a self-contained reproduction for Pyro issue 3061.

The bug is an import-time failure in `pyro/distributions/torch_patch.py` when
`torch.distributions.constraints._CorrCholesky` is missing. The repro uses a
minimal in-memory `torch` stub so the failure is deterministic and does not
depend on the local PyTorch installation.

Files:
- `repro.py` - minimal failing reproduction
- `run_repro.sh` - shell entry point for the repro
- `setup_env.sh` - no-op setup hook for standardized runners
- `requirements.txt` - empty, because the repro only uses the standard library
- `reproduction.json` - machine-readable reproduction result
- `repro_stdout.log` / `repro_stderr.log` - captured command output

Run locally:
```bash
bash run_repro.sh
```


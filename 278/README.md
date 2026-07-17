# Bug 278

This folder contains a self-contained repro bundle for Pyro issue 3430.

Bug summary:
- serializing an `EasyGuide` subclass with `torch.save` corrupts the original guide instance
- the deserialized guide still works

Verified locally with:
- Python `3.12.3`
- Torch `2.6.0`
- local source in `codebase/`

Run:
`bash run_repro.sh`

Generated files:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reference:
- issue URL: `https://github.com/pyro-ppl/pyro/issues/3430`

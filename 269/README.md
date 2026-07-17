# Bug 269

This folder is a standalone reproduction bundle for the Lightning checkpoint
`_instantiator` issue described in `bug_report.txt`.

What is included:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- A checkpoint with plain `dict`/`str` hyperparameters loads successfully with
  `torch.load(..., weights_only=True)`.
- `LightningModule.load_from_checkpoint()` still imports and calls the
  attacker-controlled `_instantiator` value from `hyper_parameters`.
- The repro writes `imported.txt` and `called.txt` from the payload module.

Run:
```bash
bash run_repro.sh
```

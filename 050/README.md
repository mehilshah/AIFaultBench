# Bug 050

Reproduction bundle for Keras issue [#1898](https://github.com/keras-team/keras-io/issues/1898).

Files:
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

Run:
```bash
bash setup_env.sh
bash run_repro.sh
```

The repro uses the torch backend and a synthetic `torch.utils.data.DataLoader`
to exercise the same `GAN.train_step()` path described in the bug report.

# Bug 292

Reproduction bundle for https://github.com/pytorch/rl/issues/3881.

Observed behavior:
- `OpenSpielEnv("chess", return_state=True, batch_size=(100,))` raises
  `ValueError: The value of spec.shape (torch.Size([1])) must match the env batch size (torch.Size([100])).`
- The failure happens during environment construction, before `reset()`.

Files in this folder:
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

How to run:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

The run captures stdout and stderr into `repro_stdout.log` and `repro_stderr.log`.

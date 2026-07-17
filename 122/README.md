# Bug 122

This folder contains a standalone repro bundle for the SB3 `net_arch=None`
save/load crash described in `bug_report.txt`.

Included source inputs:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Repro summary:
- issue URL: `https://github.com/DLR-RM/stable-baselines3/issues/1928`
- library: `stable_baselines3`
- library version from bundle: `2.4.0a1`
- failure site: `stable_baselines3/common/base_class.py:695`

# Bug 228

This folder contains a self-contained repro for the POT unbalanced Sinkhorn regression described in `bug_report.txt`.

What the repro does:
- loads the local `codebase/ot/unbalanced/_sinkhorn.py` implementation directly
- runs the exact 2x2 example from the report
- prints the resulting transport plan and whether it matches the `0.9.4` or `0.9.5` values from the issue

Files generated for the repro:
- `local_ot_loader.py`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction command:
`bash run_repro.sh`

Verified result in this folder:
- the local source tree produces `[[0.32205361, 0.1184769], [0.1184769, 0.32205361]]`
- that matches the `POT==0.9.5` value from the bug report
- the `POT==0.9.4` control value is `[[0.51122814, 0.18807032], [0.18807032, 0.51122814]]`

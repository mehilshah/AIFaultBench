# Bug 519

This folder contains a standardized reproduction bundle for the GraphGym
import failure reported in PyG issue `#10018`.

The reproducer is intentionally minimal:
- it mirrors the relevant `torch_geometric.graphgym` package layout from the
  local `codebase/`
- it omits `torch_geometric/graphgym/imports.py`
- it imports `torch_geometric.graphgym.imports` to trigger the reported
  `ModuleNotFoundError`

Files in this bundle:
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

Expected outcome:
- the run prints the `ModuleNotFoundError` for
  `torch_geometric.graphgym.imports`
- `reproduction.json` records whether the bug is reproducible here

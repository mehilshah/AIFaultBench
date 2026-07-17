# Bug 606

This folder is the reusable standardized repro bundle for PyG issue 9888.

Inputs reused from the standardized bug folder:
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

Reproduction summary:
- issue URL: `https://github.com/pyg-team/pytorch_geometric/issues/9888`
- local source snapshot: `ab2b458f0c0f72d3cb573350b324db563066a7ee`
- observed failure: `ToyModel.forward() got multiple values for argument 'data'`
- status: reproducible in this folder

Run:
`bash run_repro.sh`

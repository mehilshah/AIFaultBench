# Bug 432

This folder is the reusable standardized benchmark input for bug 432.

Reused inputs:
- `bug_report.txt`
- `codebase/` from `pyg-team/pytorch_geometric@69193c895fe721fb45e63985bb79e8d130ee7782`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

What fails:
- `torch_geometric.contrib.explain.PGMExplainer` lazily imports `pgmpy.estimators.CITests.chi_square`.
- On Python 3.9, `pgmpy==1.0.0` raises `TypeError: unsupported operand type(s) for |: 'type' and 'type'` while importing `pgmpy/base/DAG.py`.
- That matches the CI failure described in `bug_report.txt`.

Run the repro:
`bash run_repro.sh`

Useful source references:
- `codebase/torch_geometric/contrib/explain/pgm_explainer.py`
- `codebase/test/contrib/explain/test_pgm_explainer.py`

# Bug 069

This folder is the reusable standardized benchmark input for Keras-IO issue 1489.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- The example's `show_heatmap(df)` call reaches `plt.matshow(data.corr())`.
- With the `Date Time` string column still present, pandas raises `ValueError: could not convert string to float`.
- Verified locally in a venv with `pandas 3.0.3` and `matplotlib 3.11.0`.

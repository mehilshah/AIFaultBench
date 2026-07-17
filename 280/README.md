# Bug 280

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/` when available

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- issue URL: `https://github.com/PythonOT/POT/issues/418`
- commit hash: `0411ea22a96f9c22af30156b45c16ef39ffb520d`
- library: `POT`
- tested codebase version: `0.8.3dev`
- bug type: wrong normalization when `projections=` is provided to `ot.sliced.sliced_wasserstein_distance`

How to run:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

Observed result:
- identical projection matrices are returned for the seeded and explicit-projection calls
- the costs differ because the explicit-projection path divides by the default projection count instead of the provided projection count
- seeded call: `21.887428414187593`
- custom-projection call: `9.788355557356775`

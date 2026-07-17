# Bug 111

This folder contains the reusable standardized reproduction bundle for PyGAD issue 335.

Inputs:
- `bug_report.txt`
- `codebase/`

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- issue URL: `https://github.com/ahmedfgad/GeneticAlgorithmPython/issues/335`
- library: `pygad`
- library version: `3.5.0`
- result: reproducible
- observed failure mode: integer gene values drift below `init_range_low=0`

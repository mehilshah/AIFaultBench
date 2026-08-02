# Bug 740

Phoenix's ATIF validator accepts a present but malformed step timestamp, after which the converter crashes in `datetime.fromisoformat`. The offline repro asserts the exact `ValueError`; on this host it prints a bug marker and exits with status 1, confirming the fault.

Files: `repro.py` is the minimal trigger, `requirements.txt` pins its dependencies, `setup_env.sh` builds the environment, `run_repro.sh` runs it, and the logs and reproduction metadata record the observed result.

Run after recreating the checkout:

```bash
bash setup_codebase.sh
bash run_repro.sh
```

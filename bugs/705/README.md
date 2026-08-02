# Bug 705

This bundle examines the claim that DSPy's GEPA ignores `reflection_minibatch_size`. The issue reporter withdrew that claim: DSPy forwards the value to GEPA, whose sampler limits every reflection batch before the DSPy adapter sees it. The deterministic repro uses a recording adapter and no LLM, API key, or network call.

On this host the fault is not reproduced: DSPy 3.0.4 forwards `3` and GEPA 0.0.17 creates only three-trajectory reflection batches.

Files: `repro.py` performs the check; `requirements.txt` pins the released issue-era packages; `setup_env.sh` creates the virtual environment; `run_repro.sh` runs the check; output is in `repro_stdout.log` and `repro_stderr.log`; and `reproduction.json`/`reproduction_trajectory.md` record the evidence.

Run:

```bash
bash run_repro.sh
```

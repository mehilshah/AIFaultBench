# Bug 706

DSPy's buggy reasoning-model regex classifies `azure/gpt-5-chat` as a reasoning model. The offline repro constructs that LM with normal chat settings and checks that DSPy raises its inappropriate reasoning-model validation error. The fault is reproduced on this host without any Azure or LLM API call.

Files: `repro.py` is the minimal trigger; `requirements.txt`, `setup_env.sh`, and `run_repro.sh` create and run the environment; `repro_stdout.log` and `repro_stderr.log` contain final-run evidence; `reproduction.json` and `reproduction_trajectory.md` record the result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```

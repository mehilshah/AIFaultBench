# Bug 763

At the pinned DSPy checkout, the documented-looking `dspy.AzureOpenAI` symbol is not exported. The deterministic repro imports DSPy and verifies that looking up this attribute raises the reported `AttributeError`, without model credentials or provider calls. The fault reproduces on this host.

Files: `repro.py` is the assertion-based reproducer; `requirements.txt` pins its dependencies; `setup_env.sh` builds the virtual environment; `run_repro.sh` is the entrypoint; the logs contain the final captured run; `reproduction.json` and `reproduction_trajectory.md` record the evidence.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```

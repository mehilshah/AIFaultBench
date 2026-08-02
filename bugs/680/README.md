# Bug 680

CAMEL 0.2.82 crashes while handling a streamed usage chunk whose `completion_tokens` is `None`: the token tracker adds that null value to its integer counter. The offline reproduction injects that usage-only chunk into ChatAgent's actual streaming accumulator in the pinned checkout and verifies the reported `TypeError`, without making a model/provider call. This host reproduced the fault at `b7a2fda98db44d7b3feeda9259ef09ae0b0de8b5`.

Files: `repro.py` is the deterministic reproducer; `requirements.txt` contains the pinned package inputs; `setup_env.sh` creates the venv; `run_repro.sh` runs it; and `repro_stdout.log` / `repro_stderr.log` contain final-run evidence. `reproduction.json` and `reproduction_trajectory.md` record the result.

Run:

```bash
bash run_repro.sh
```

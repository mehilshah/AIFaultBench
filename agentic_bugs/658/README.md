# Bug 658

`Fireworks._acall` formats an aiohttp error with the `response.text` method
instead of awaiting it. The offline repro substitutes a deterministic 400
response and checks that the resulting `ValueError` contains the bound-method
representation rather than its JSON error body. The bug reproduces on this
host with the issue-era `langchain-fireworks==1.4.4` release.

Files: `repro.py` is the failing reproducer, `requirements.txt` pins its
dependencies, `setup_env.sh` creates the virtual environment, `run_repro.sh`
runs it, and the two log files contain the final captured run.

Run:

```bash
bash run_repro.sh
```

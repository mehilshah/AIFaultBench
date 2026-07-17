# Reproduction Trajectory — Bug 222: towhee

- **Bug report:** [https://github.com/towhee-io/towhee/issues/2714](https://github.com/towhee-io/towhee/issues/2714)
- **Repository:** towhee-io/towhee @ `fe85630`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an isolated virtual environment and install `requirements.txt`.
2. Run `bash run_repro.sh` with `PYTHONPATH` pointing at the local `codebase/` snapshot.
3. Observe the constructor failure when the local Triton client wrapper instantiates `aio_httpclient.InferenceServerClient`.

## Observed behavior

- `bash run_repro.sh` completed the isolated environment setup and then loaded `towhee.serve.triton.pipeline_client.Client` from `codebase/towhee/serve/triton/pipeline_client.py`.
- Constructing `Client('127.0.0.1:8000')` raised `RuntimeError: no running event loop` from `aiohttp/connector.py` inside `tritonclient.http.aio.InferenceServerClient`.
- The traceback pinpoints the local source line `codebase/towhee/serve/triton/pipeline_client.py:55` as the call site.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

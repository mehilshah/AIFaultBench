# Reproduction Trajectory — Bug 669: pydantic-ai

- **Bug report:** [https://github.com/pydantic/pydantic-ai/issues/6611](https://github.com/pydantic/pydantic-ai/issues/6611)
- **Repository:** pydantic/pydantic-ai @ `fa0ec68b551a5940ac32b0a5593b965c7c84fd6b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and confirmed the generated checkout at `fa0ec68b551a5940ac32b0a5593b965c7c84fd6b`. The initial clone had no fetched commits, so I fetched that explicit commit and checked it out before proceeding.
2. Created `.venv`, installed the exact dependencies in `requirements.txt`, and installed `codebase/pydantic_ai_slim` editable without resolving its unreleased checkout version as a package dependency.
3. Ran `bash run_repro.sh`. `repro.py` instantiates the pinned `OpenAIResponsesModel` for `gpt-5.6-sol` with a fake SDK client; its local `responses.retrieve()` implementation represents OpenAI's persisted endpoint and makes no network requests.

## Observed behavior

- The pinned retrieval path supplied `reasoning.encrypted_content` to the fake persisted endpoint.
- The fake endpoint returned the reported 400 message, which the library mapped to `ModelHTTPError`: `status_code: 400, model_name: gpt-5.6-sol, body: {'message': 'Encrypted content cannot be requested for persisted responses.', 'type': 'invalid_request_error', 'param': 'include'}`.
- `run_repro.sh` exited with status 1, deliberately signalling that the buggy behavior is present.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

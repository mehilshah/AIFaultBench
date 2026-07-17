# Reproduction Trajectory — Bug 351: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/48097](https://github.com/vllm-project/vllm/issues/48097)
- **Repository:** vllm-project/vllm @ `ab7961a14a59be9a0170f1654315d5c2be44c015`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a minimal Pydantic reproducer mirroring the request/response field mismatch from codebase/vllm/entrypoints/openai/responses/protocol.py.
2. Installed pydantic into a local virtual environment with ./setup_env.sh.
3. Ran ./run_repro.sh and captured stdout/stderr in repro_stdout.log and repro_stderr.log.
4. Observed the expected ValidationError when None was passed into the response model.

## Observed behavior

- request.parallel_tool_calls=None was accepted by the request-side model.
- ResponsesResponse.model_validate({'parallel_tool_calls': None}) raised a Pydantic ValidationError: Input should be a valid boolean [type=bool_type, input_value=None, input_type=NoneType].
- The captured output matches the bug report's crash mode for parallel_tool_calls=null.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

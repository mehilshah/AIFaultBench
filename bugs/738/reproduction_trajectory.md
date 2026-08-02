# Reproduction Trajectory — Bug 738: phoenix

- **Bug report:** [https://github.com/Arize-ai/phoenix/issues/13934](https://github.com/Arize-ai/phoenix/issues/13934)
- **Repository:** Arize-ai/phoenix @ `7afa18317c18142d7eb772682bc9369b10cf0e2e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`, then checked out the pinned commit after a shallow fetch because the initial full clone did not complete in the reference environment.
2. Created an isolated Python 3.12 virtual environment and installed the exact pinned dependencies and the checkout in editable mode.
3. Used `BedrockStreamingClient._converse_build_request` with the bare raw tool stored by the Bedrock instrumentation.
4. Sent the resulting dictionary to botocore's parameter validator with its request transport replaced by an assertion, ensuring no AWS request can occur.

## Observed behavior

- Phoenix emitted `{'name': 'weather', 'description': 'reports weather', 'inputSchema': {'json': {'type': 'object'}}}` as `toolConfig.tools[0]`, without a `toolSpec` wrapper.
- botocore raised `ParamValidationError`: `Invalid number of parameters set for tagged union structure toolConfig.tools[0]` and identified `name`, `description`, and `inputSchema` as unknown keys.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

# Reproduction Trajectory — Bug 677: semantic-kernel

- **Bug report:** [https://github.com/microsoft/semantic-kernel/issues/13174](https://github.com/microsoft/semantic-kernel/issues/13174)
- **Repository:** microsoft/semantic-kernel @ `e73446e86e318f4c437aa7f49ece8c6ba3afba43`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified the checkout was at the pinned Semantic Kernel 1.37.0 commit.
2. Installed the pinned offline dependencies, including `opentelemetry-instrumentation-openai-v2==2.1b0`, then installed the checkout editable.
3. Ran `bash run_repro.sh`. The repro returns the instrumentation package's real `StreamWrapper` from a fake asynchronous `chat.completions.create` method, so no provider request, credentials, or network I/O occurs.
4. Semantic Kernel's `OpenAIHandler._send_completion_request` called `store_usage` before returning the stream; its non-`AsyncStream` branch accessed `response.usage` on the wrapper.

## Observed behavior

- `run_repro.sh` exited with status 1.
- The captured stdout was `OBSERVED BUG: AttributeError: 'StreamWrapper' object has no attribute 'usage'`.
- The final captured stderr was empty.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

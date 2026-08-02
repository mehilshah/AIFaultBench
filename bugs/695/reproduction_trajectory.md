# Reproduction Trajectory — Bug 695: llama_index

- **Bug report:** [https://github.com/run-llama/llama_index/issues/21086](https://github.com/run-llama/llama_index/issues/21086)
- **Repository:** run-llama/llama_index @ `31a502c4fa1c6aae0acb52448b730732678847da`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`; because the full LlamaIndex monorepo checkout was impractically large on this host, used the published issue-era integration package instead, and fetched the affected file object at the pinned commit for source verification.
2. Installed the released issue-era package `llama-index-llms-ollama==0.10.0` and `ollama==0.5.4` in an isolated virtual environment. The installed affected source file was byte-for-byte identical to the pinned checkout's source (`SHA-256 1a204455713992e77c94f557c98aa024b60e6e45d90d8a458de72e5bb52f02f1`).
3. Passed an authenticated async-client double to `Ollama`, replaced the internally constructed synchronous `Client` with an offline stub, and invoked `llm.complete("hi")`.
4. Asserted that the supplied async client remained stored while exactly one new synchronous client with an empty header set was constructed; the stub raised the protected-server response deterministically.

## Observed behavior

- `bash run_repro.sh` exited with status 1.
- The repro printed `BUG OBSERVED: sync complete ignored supplied async-client Authorization headers`.
- No network request was made: the client class used only for the unexpected sync-client construction was replaced before `complete()` was invoked.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

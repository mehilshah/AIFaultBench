# Reproduction Trajectory — Bug 748: langgraph

- **Bug report:** [https://github.com/langchain-ai/langgraph/issues/6578](https://github.com/langchain-ai/langgraph/issues/6578)
- **Repository:** langchain-ai/langgraph @ `df191731918482c5eaf2934a2df0c9cb3571db0c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Read the report and its maintainer discussion, which identifies the LangChain 1.1.0 and LangGraph 1.0.4 release environment.
2. Ran `bash setup_codebase.sh` twice. Under concurrent benchmark load, the full clone did not finish creating a checkout, so used the permitted issue-era released-package fallback.
3. Created `.venv` and installed the fully pinned LangChain 1.1.0 / LangGraph 1.0.4 dependency set.
4. Ran a local fake chat model that emits one `clarify_user` tool call. The tool returns `Command(goto="__end__")` while updating messages with a `ToolMessage` followed by an `AIMessage`.
5. Made the fake model signal an observed fault only if invoked after the tool's terminal command, then ran `bash run_repro.sh`.

## Observed behavior

- `run_repro.sh` exited with status 1.
- Standard output reported `OBSERVED: Command(goto='__end__') did not stop the agent loop`.
- The script reaches the nonzero fault path only when its fake model sees a second call after the terminal command, proving the extra model invocation without a provider call.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

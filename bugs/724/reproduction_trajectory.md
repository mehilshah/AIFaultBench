# Reproduction Trajectory — Bug 724: crewAI

- **Bug report:** [https://github.com/crewAIInc/crewAI/issues/5620](https://github.com/crewAIInc/crewAI/issues/5620)
- **Repository:** crewAIInc/crewAI @ `cb46a1c4babef8c51db6499d7a81f2c36b01bdef`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`; the repository completed at the pinned commit.
2. Created `.venv`, installed the 1.14.3 dependency set, and installed `codebase/lib/crewai` editable so the repro imports the pinned checkout.
3. Created a local `Agent`, `Crew`, and `Task` whose `guardrails` contains one local function; no crew kickoff or LLM call occurs.
4. Built a `RuntimeState` containing the crew and invoked `model_dump(mode="json")`, the same JSON serialization operation used by the auto-checkpoint listener.

## Observed behavior

- `RuntimeState` serialization raised `pydantic_core._pydantic_core.PydanticSerializationError: Unable to serialize unknown type: <class 'function'>`.
- The local reproduction disables outbound socket connections before importing CrewAI and does not invoke a model provider.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

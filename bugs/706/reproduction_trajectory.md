# Reproduction Trajectory — Bug 706: dspy

- **Bug report:** [https://github.com/stanfordnlp/dspy/issues/9032](https://github.com/stanfordnlp/dspy/issues/9032)
- **Repository:** stanfordnlp/dspy @ `ba32809e730d9c35969a4d899fde0305344638a1`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Cloned the repository with `bash setup_codebase.sh` and verified the pinned buggy commit.
2. Created an isolated virtual environment and installed the editable pinned checkout.
3. Constructed `dspy.LM("azure/gpt-5-chat", temperature=0.7, max_tokens=1000)`. This constructor-only path makes no LLM or Azure request.

## Observed behavior

- The constructor raised the reasoning-model validation `ValueError` for `azure/gpt-5-chat`, even though that model is a chat model.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

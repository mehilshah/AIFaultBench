# Reproduction Trajectory — Bug 744: autogen

- **Bug report:** [https://github.com/microsoft/autogen/issues/6551](https://github.com/microsoft/autogen/issues/6551)
- **Repository:** microsoft/autogen @ `446da624ac091562f4055344b36e6e2115ae5727`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`; the checkout was placed at the requested pinned commit.
2. Created `.venv` and installed the local `autogen-core` and `autogen-agentchat` 0.5.7 packages with their pinned runtime dependencies.
3. Replaced model-backed agents with deterministic local `ScriptedAgent` objects. B emits `SEARCH_AGAIN` once, then `NOT_FOUND`, taking A -> B -> A -> B -> D.
4. Added the issue's C -> E and D -> E edges with E's default `all` activation, then ran `bash run_repro.sh` and captured its output.

## Observed behavior

- `run_repro.sh` exited with status 1.
- The script printed `OBSERVED: RuntimeError: No available speakers found.`
- The captured traceback raises that error from `autogen_agentchat/teams/_group_chat/_graph/_digraph_group_chat.py:357` after D completes; E remains blocked waiting for the unchosen C branch.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

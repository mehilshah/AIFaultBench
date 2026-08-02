# Reproduction Trajectory — Bug 746: langchain

- **Bug report:** [https://github.com/langchain-ai/langchain/issues/37736](https://github.com/langchain-ai/langchain/issues/37736)
- **Repository:** langchain-ai/langchain @ `84e3c795ec292cd32156f65c37c1445abb94b576`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Read the issue report and comments, which identify the divergent async normalization in `arank_fusion`.
2. Ran `bash setup_codebase.sh`; its generated checkout was then fetched at the required pinned commit because the initial clone had no valid `HEAD`.
3. Created `.venv`, installed the exact requirements, and installed the pinned `core`, `text-splitters`, and `langchain-classic` source packages editable.
4. Ran `bash run_repro.sh` with a local `BaseRetriever` that returns `[42]` from its async method.

## Observed behavior

- `arank_fusion` at `ensemble.py:297` calls `Document(page_content=42)`.
- The final run printed `BUG OBSERVED: async arank_fusion rejected integer 42 as Document.page_content` and raised `pydantic_core._pydantic_core.ValidationError`: `page_content` must be a valid string and its input value was `42`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

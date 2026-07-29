# Reproduction Trajectory — Bug 693: llama_index

- **Bug report:** [https://github.com/run-llama/llama_index/issues/21109](https://github.com/run-llama/llama_index/issues/21109)
- **Repository:** run-llama/llama_index @ `c346327e51eaf26c84a495f8bee1f9ea81542bc7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`. The upstream clone did not finish on this host and left an unborn Git repository, so the issue-reported release `llama-index-core==0.14.18` was pinned instead.
2. Inspected that release's `SimplePropertyGraphStore.persist`, which calls `fs.open(persist_path, "w")` with no encoding.
3. Created a graph store with a Chinese entity name (`定义`) and persisted it through a small filesystem double that opens text files with Windows cp1252, requiring no model or external service.
4. Ran `bash run_repro.sh` and captured the output.

## Observed behavior

- The process exited with status 1 after `SimplePropertyGraphStore.persist` raised `UnicodeEncodeError: 'charmap' codec can't encode characters in position 11-12: character maps to <undefined>`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

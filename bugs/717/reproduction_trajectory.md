# Reproduction Trajectory — Bug 717: SWE-agent

- **Bug report:** [https://github.com/SWE-agent/SWE-agent/issues/1012](https://github.com/SWE-agent/SWE-agent/issues/1012)
- **Repository:** SWE-agent/SWE-agent @ `ec75580fe90f198bce2730e3642f33f5874f3357`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and checked out `ec75580fe90f198bce2730e3642f33f5874f3357`.
2. Inspected the pinned `sweagent.utils.log.add_file_handler` helper and confirmed it creates `logging.FileHandler(path)` without selecting UTF-8.
3. Created `.venv`, installed the minimal pinned logging dependency set, and installed the checkout editable with no dependency resolution.
4. Ran `bash run_repro.sh`; the script loaded the pinned helper and supplied cp1252 as the platform-default encoding only when its `FileHandler` call omitted an encoding.
5. Captured the resulting non-zero run in the evidence logs.

## Observed behavior

- The helper's log handler used `cp1252`, then failed to write `🤖 MODEL INPUT`.
- `repro_stderr.log` reports `UnicodeEncodeError: 'charmap' codec can't encode character '\\U0001f916'` from `encodings/cp1252.py`.
- The reproduction printed `OBSERVED BUG: UnicodeEncodeError for U+1F916 with cp1252 FileHandler` and exited with status 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

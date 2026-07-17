# Reproduction Trajectory — Bug 107: adapters

- **Bug report:** [https://github.com/adapter-hub/adapters/issues/748](https://github.com/adapter-hub/adapters/issues/748)
- **Repository:** adapter-hub/adapters @ `6fefc9a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the isolated environment with `bash setup_env.sh`.
2. Run `bash run_repro.sh` from the standardized bug folder.
3. Observe that importing `LoRAConfig` fails while `huggingface-hub==0.26.0` is installed.

## Observed behavior

- Running `bash run_repro.sh` returns exit code 1 and the logs show `from adapters import LoRAConfig` fails with `RuntimeError: Failed to import adapters.configuration ... cannot import name 'url_to_filename' from 'huggingface_hub.file_download'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

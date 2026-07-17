# Reproduction Trajectory — Bug 154: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/42925](https://github.com/huggingface/transformers/issues/42925)
- **Repository:** huggingface/transformers @ `171e079`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Set up the local virtual environment with bash setup_env.sh.
2. Run bash run_repro.sh.
3. Observe the traceback in repro_stderr.log and the nonzero exit recorded by the repro script.

## Observed behavior

- Running the local repro creates TvpConfig without type_vocab_size, then TvpModel(config) raises AttributeError: 'TvpConfig' object has no attribute 'type_vocab_size' from transformers/models/tvp/modeling_tvp.py:297.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```

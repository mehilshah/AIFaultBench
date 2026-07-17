# Reproduction Trajectory — Bug 153: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/42913](https://github.com/huggingface/transformers/issues/42913)
- **Repository:** huggingface/transformers @ `dd24a80`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an isolated virtual environment and install the tokenizer/runtime dependencies from `requirements.txt`.
2. Run `repro.py` with `PYTHONPATH=codebase/src` so the local `transformers` source is used.
3. Observe that `AutoTokenizer.decode([128000, 64, 1174, 65])` returns '<|begin_of_text|>a ,b'.

## Observed behavior

- Running the local source tree against `mlx-community/Llama-3.2-1B-Instruct-4bit` decodes `[128000, 64, 1174, 65]` to '<|begin_of_text|>a ,b' instead of the reported v4 output '<|begin_of_text|>a,b'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

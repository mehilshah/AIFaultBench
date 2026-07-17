# Reproduction Trajectory — Bug 267: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/47337](https://github.com/huggingface/transformers/issues/47337)
- **Repository:** huggingface/transformers @ `498d6e984e84d29186e671656817a53a024af930`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a tiny LayoutLM config with max_2d_position_embeddings=1001.
2. Passed a bbox tensor containing the value 1001 into LayoutLMModel.forward().
3. Observed the model raise IndexError from the bbox embedding lookup path.

## Observed behavior

- bash run_repro.sh exits 1 and repro_stderr.log shows IndexError: The `bbox`coordinate values should be within 0-1000 range from codebase/src/transformers/models/layoutlm/modeling_layoutlm.py:102.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```

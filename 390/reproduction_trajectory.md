# Reproduction Trajectory — Bug 390: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/47050](https://github.com/huggingface/transformers/issues/47050)
- **Repository:** huggingface/transformers @ `b70d02fc724d04c916832ca4ead03ff05e8fb1ee`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the isolated environment with `bash setup_env.sh`.
2. Run the repro with `bash run_repro.sh`.
3. Observe the dtype mismatch traceback in `repro_stderr.log` and the version banner in `repro_stdout.log`.

## Observed behavior

- Running `bash run_repro.sh` in the recreated `codebase/` snapshot fails while tracing `torch.onnx.export(...)` with `RuntimeError: expected m1 and m2 to have the same dtype, but got: float != c10::Half`. The traceback points to `codebase/src/transformers/models/canine/modeling_canine.py:353` at `context_layer = torch.matmul(attention_probs, value_layer)`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

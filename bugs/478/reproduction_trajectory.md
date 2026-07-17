# Reproduction Trajectory — Bug 478: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/46897](https://github.com/huggingface/transformers/issues/46897)
- **Repository:** huggingface/transformers @ `c96378c4136f5882fee50d8ff8ee1e9588a17eb6`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Build a tiny random Florence2ForConditionalGeneration model from the local transformers checkout.
2. Run a forward pass with synthetic input_ids and labels.
3. Compare the returned loss against direct cross-entropy on labels and against shifted-label cross-entropy.

## Observed behavior

- Florence2ForConditionalGeneration.loss_function is ForCausalLMLoss; model loss=2.348682880, direct CE on labels=2.449419260, shifted-label CE=2.348682880.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```

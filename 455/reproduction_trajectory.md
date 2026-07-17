# Reproduction Trajectory — Bug 455: peft

- **Bug report:** [https://github.com/huggingface/peft/issues/297](https://github.com/huggingface/peft/issues/297)
- **Repository:** huggingface/peft @ `cc82b674b5db38b9a393463d38afe66e8f48ac1c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Build a tiny 2048x2048 LoRA-wrapped linear layer from the local PEFT source.
2. Verify merge_and_unload() works on the unsharded control model.
3. Replace the target weight with a ZeRO-3-like shard shaped [2048, 0].
4. Call merge_and_unload() again and observe the tensor-size RuntimeError.

## Observed behavior

- merge_and_unload succeeded on an unsharded control model, then failed after the target weight was shrunk to a zero-width shard. The failure was: RuntimeError: The size of tensor a (0) must match the size of tensor b (2048) at non-singleton dimension 1

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```

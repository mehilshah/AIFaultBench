# Reproduction Trajectory — Bug 367: peft

- **Bug report:** [https://github.com/huggingface/peft/issues/868](https://github.com/huggingface/peft/issues/868)
- **Repository:** huggingface/peft @ `8c17d556a8fe9522e10d73d7bd3fad46a6ecae14`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Load sshleifer/tiny-gpt2.
2. Dispatch one transformer block to disk so the model contains meta tensors.
3. Attach a LoRA adapter and call merge_and_unload().
4. Call save_pretrained() on the merged model.

## Observed behavior

- save_pretrained failed with TypeError: 'NoneType' object is not subscriptable
- meta parameters stayed present after merge (12 meta tensors)

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

# Reproduction Trajectory — Bug 302: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/3487](https://github.com/huggingface/accelerate/issues/3487)
- **Repository:** huggingface/accelerate @ `63168b151fa15987064a22c77b8b8ec72946f54e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the repro bundle files in the standardized folder.
2. Run bash run_repro.sh against the local accelerate codebase snapshot.
3. Inspect repro_stdout.log and repro_stderr.log for the FSDP2 unwrap and safetensors failure.

## Observed behavior

- run_repro.sh exited with status 1 after entering an FSDP distributed run with fsdp_version=2.
- The unwrapped model type was FSDPGPT2LMHeadModel and it still had no plain module attribute, while its state_dict sample entries were DTensor values.
- safetensors.torch.save_file(state_dict, ...) failed with RuntimeError: Attempted to access the data pointer on an invalid python storage.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

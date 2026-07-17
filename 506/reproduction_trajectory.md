# Reproduction Trajectory — Bug 506: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/14175](https://github.com/huggingface/diffusers/issues/14175)
- **Repository:** huggingface/diffusers @ `01969142b55379991fee07608c9e7e8f80afced0`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local AutoencoderTiny checkpoint with sharded safetensors.
2. Moved one shard outside the model directory and rewrote the index weight_map entry to ../outside/secret.safetensors.
3. Confirmed _get_checkpoint_shard_files returned the escaped path and from_pretrained loaded the model successfully.

## Observed behavior

- A local sharded AutoencoderTiny checkpoint was rewritten so diffusion_pytorch_model.safetensors.index.json mapped one shard to ../outside/secret.safetensors. _get_checkpoint_shard_files resolved that shard to an out-of-directory path, and AutoencoderTiny.from_pretrained loaded successfully from the outside copy after the in-tree shard was removed.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

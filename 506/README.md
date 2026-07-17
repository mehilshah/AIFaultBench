# Bug 506

This folder reproduces the diffusers shard-index path traversal bug described in `bug_report.txt`.

## What the repro does

`repro.py` creates a local sharded `AutoencoderTiny` checkpoint, rewrites one entry in `diffusion_pytorch_model.safetensors.index.json` to `../outside/secret.safetensors`, deletes the in-tree shard, and then calls `AutoencoderTiny.from_pretrained(...)`.

The loader still resolves and opens the out-of-directory shard.

## Run

```bash
./run_repro.sh
```

## Outputs

- `repro_stdout.log`
- `repro_stderr.log`
- `reproduction.json`

## Notes

- The repro uses the local `codebase/src` checkout through `PYTHONPATH`.
- No Hub access is required.

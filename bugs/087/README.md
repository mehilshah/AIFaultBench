# Bug 087 Reproduction Bundle

This folder reproduces the `x-transformers` flash-attention bug described in `bug_report.txt`.

## What fails

Calling `Decoder(..., alibi_pos_bias=True, attn_flash=True)` with custom positions passed as a 2D tensor raises:

`einops.EinopsError: Error while processing rearrange-reduction pattern "h i j -> 1 h i j". Input tensor shape: torch.Size([2, 8, 4, 4]).`

The failure occurs in `codebase/x_transformers/attend.py:373`.

## How to run

```bash
bash run_repro.sh
```

The script writes:

- `repro_stdout.log`
- `repro_stderr.log`
- `reproduction.json`

## Included files

- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`

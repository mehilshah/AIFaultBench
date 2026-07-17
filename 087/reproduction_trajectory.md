# Reproduction Trajectory — Bug 087: x-transformers

- **Bug report:** [https://github.com/lucidrains/x-transformers/issues/298](https://github.com/lucidrains/x-transformers/issues/298)
- **Repository:** lucidrains/x-transformers @ `57efd7770f2f5df0ff7b4ffcbd623750b584e850`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. python repro.py

## Observed behavior

- Running Decoder(dim=512, depth=2, heads=8, alibi_pos_bias=True, attn_flash=True) with a 2D custom pos tensor raises einops.EinopsError in codebase/x_transformers/attend.py:373: Error while processing rearrange-reduction pattern 'h i j -> 1 h i j'. Input tensor shape: torch.Size([2, 8, 4, 4]).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

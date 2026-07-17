# Reproduction Trajectory — Bug 104: vector-quantize-pytorch

- **Bug report:** [https://github.com/lucidrains/vector-quantize-pytorch/issues/160](https://github.com/lucidrains/vector-quantize-pytorch/issues/160)
- **Repository:** lucidrains/vector-quantize-pytorch @ `54d29e8fba72443a29928e9f94ee52ca43eeb60a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment with `./setup_env.sh` and installed `torch`, `einops`, and `einx`.
2. Ran `./run_repro.sh` against `codebase/vector_quantize_pytorch/residual_vq.py`.
3. Observed that `ResidualVQ(dim=8, num_quantizers=4, codebook_size=16, implicit_neural_codebook=False)` still initializes 3 MLP modules.

## Observed behavior

- Running `bash run_repro.sh` prints `implicit_neural_codebook=False` and `initialized_mlps=3`, then raises `AssertionError: ResidualVQ initialized MLP modules even though implicit_neural_codebook=False`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

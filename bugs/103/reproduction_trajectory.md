# Reproduction Trajectory — Bug 103: vector-quantize-pytorch

- **Bug report:** [https://github.com/lucidrains/vector-quantize-pytorch/issues/188](https://github.com/lucidrains/vector-quantize-pytorch/issues/188)
- **Repository:** lucidrains/vector-quantize-pytorch @ `59a30b68a83be710638184764c025b54693c82cc`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local venv with `./setup_env.sh` and installed `torch`, `einops`, and `einx`.
2. Ran `./run_repro.sh`, which instantiates `ResidualLFQ(dim=14, num_quantizers=1, codebook_size=16384, commitment_loss_weight=1.0)` on `x.shape=(2, 1851, 14)` with a boolean mask containing two `False` entries.
3. Observed one matching UserWarning and recorded the run output in `repro_stdout.log` and `repro_stderr.log`.

## Observed behavior

- Running `./run_repro.sh` emitted a UserWarning from `codebase/vector_quantize_pytorch/lookup_free_quantization.py:397`: target size `torch.Size([2, 1851, 1, 14])` vs input size `torch.Size([3700, 14])` during `F.mse_loss(original_input, quantized.detach(), reduction='none')`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

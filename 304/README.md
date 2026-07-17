# Bug 304 Reproduction

This bundle reproduces the bug described in `bug_report.txt` by statically
inspecting the FlashInfer allreduce + RMSNorm + quant fusion registrations in
`codebase/vllm/compilation/passes/fusion/allreduce_rms_fusion.py`.

What the repro checks:
- `AllReduceFusedAddRMSNormStaticQuantFP8Pattern`
- `AllReduceFusedAddRMSNormStaticQuantNVFP4Pattern`

These residual quant patterns are present without the dtype compatibility guard
that the neighboring non-residual quant patterns use. The bug report says this
allows mixed BF16 input / FP32 RMSNorm weights to select an unsafe fused path.

Run:

```bash
bash run_repro.sh
```

The script exits successfully when the unsafe registration is present and prints
the exact evidence to stdout.

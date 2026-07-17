# DiffusionGemma image-text-to-text repro

This bundle reproduces the `DiffusionGemmaGenerationOutput` / `image-text-to-text` pipeline mismatch described in `bug_report.txt`.

What it checks:

1. `DiffusionGemmaGenerationMixin._prepare_generation_config()` crashes when it is given a plain `GenerationConfig`.
2. `ImageTextToTextPipeline.postprocess()` crashes when it receives a `DiffusionGemmaGenerationOutput` instead of a tensor-like token sequence.

Run:

```bash
bash run_repro.sh
```

Outputs:

- `repro_stdout.log`
- `repro_stderr.log`
- `reproduction.json`

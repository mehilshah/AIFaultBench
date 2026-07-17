# Reproduction Trajectory — Bug 406: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/13979](https://github.com/huggingface/diffusers/issues/13979)
- **Repository:** huggingface/diffusers @ `3467efa65a27e4b4c3caa6e01ebb9ca035e14674`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Inspect the pinned diffusers source for `Ideogram4ModularPipeline` and the Ideogram4 LoRA mixin.
2. Run `bash run_repro.sh` to parse the source and compare the modular pipeline base classes.
3. Observe the failing check that `Ideogram4ModularPipeline` does not inherit `Ideogram4LoraLoaderMixin`.

## Observed behavior

- Pinned source defines `Ideogram4LoraLoaderMixin` with `load_lora_weights()` in `codebase/src/diffusers/loaders/lora_pipeline.py`.
- `codebase/src/diffusers/modular_pipelines/ideogram4/modular_pipeline.py` defines `Ideogram4ModularPipeline(ModularPipeline)` with no LoRA mixin.
- Repro output confirms `ideogram4_modular_pipeline_bases = ['ModularPipeline']` and `flux_modular_pipeline_bases = ['ModularPipeline', 'FluxLoraLoaderMixin', 'TextualInversionLoaderMixin']`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

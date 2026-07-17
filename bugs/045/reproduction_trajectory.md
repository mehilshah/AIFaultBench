# Reproduction Trajectory — Bug 045: fairseq

- **Bug report:** [https://github.com/facebookresearch/fairseq/issues/5320](https://github.com/facebookresearch/fairseq/issues/5320)
- **Repository:** facebookresearch/fairseq @ `b5d89cddc9e4a0af831d2aafc1ba7dbf0f1b10d0`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a structured OmegaConf config with a `model` node named `s2ut_transformer_fisher`.
2. Lock the config with `OmegaConf.set_struct(cfg, True)`.
3. Attempt to assign `cfg.model.input_feat_per_channel = 80`.
4. Observe the `ConfigAttributeError` with `full_key: model.input_feat_per_channel`.

## Observed behavior

- Running `bash run_repro.sh` raises `omegaconf.errors.ConfigAttributeError: Key 'input_feat_per_channel' is not in struct` when the script writes `cfg.model.input_feat_per_channel = 80`. The traceback matches the reported missing-key struct failure.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

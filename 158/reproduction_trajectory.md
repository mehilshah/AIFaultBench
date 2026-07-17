# Reproduction Trajectory — Bug 158: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/43479](https://github.com/huggingface/transformers/issues/43479)
- **Repository:** huggingface/transformers @ `a30413b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh

## Observed behavior

- In a clean virtualenv built from codebase/setup.py requirements, `bash run_repro.sh` prints `default_config: vision_config_is_none=True` and `vision_only_config: audio_config_is_none=True`, then raises `AssertionError` because `Phi4MultimodalConfig()` leaves `vision_config` as None and `Phi4MultimodalConfig(vision_config=Phi4MultimodalVisionConfig())` leaves `audio_config` as None. This matches the bug report and the constructor bug in `codebase/src/transformers/models/phi4_multimodal/configuration_phi4_multimodal.py`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

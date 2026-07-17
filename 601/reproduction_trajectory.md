# Reproduction Trajectory — Bug 601: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2447](https://github.com/huggingface/pytorch-image-models/issues/2447)
- **Repository:** huggingface/pytorch-image-models @ `e44f14d7d2f557b9f3add82ee4f1ed2beefbb30d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated Python 3.12 virtual environment and installed the repro dependencies.
2. Ran the local timm checkout with PYTHONPATH pointing at codebase/.
3. Executed create_model("hf-hub:google/mobilenet_v2_1.0_224", pretrained=True).

## Observed behavior

- Running create_model("hf-hub:google/mobilenet_v2_1.0_224", pretrained=True) against the local timm 1.0.15 checkout raises KeyError: 'architecture' in codebase/timm/models/_hub.py:172 when loading the Hugging Face config.json.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

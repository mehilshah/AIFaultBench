# Reproduction Trajectory — Bug 595: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/46726](https://github.com/huggingface/transformers/issues/46726)
- **Repository:** huggingface/transformers @ `9fd7b6789d0f18a57718e52aaca9d63669831625`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an isolated venv with the local transformers source on PYTHONPATH.
2. Install torch and the non-vision runtime dependencies, but do not install torchvision.
3. Run repro.py, which blocks torchvision imports and calls AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-256M-Instruct").

## Observed behavior

- With torchvision blocked, AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-256M-Instruct") raises ValueError: Unrecognized image processor in HuggingFaceTB/SmolVLM-256M-Instruct..., matching the bug report.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```

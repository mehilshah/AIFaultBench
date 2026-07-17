# Reproduction Trajectory — Bug 071: DeepSpeedExamples

- **Bug report:** [https://github.com/deepspeedai/DeepSpeedExamples/issues/934](https://github.com/deepspeedai/DeepSpeedExamples/issues/934)
- **Repository:** deepspeedai/DeepSpeedExamples @ `f73a6ed635659f03ac583a1d914ea07a2cbeab99`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python 3.12 virtual environment and install requirements.txt.
2. Run bash run_repro.sh from the standardized folder root.

## Observed behavior

- codebase/applications/DeepSpeed-Chat/dschat/utils/model/model_utils.py imports HfDeepSpeedConfig from transformers.deepspeed. With transformers==5.14.1, running the repro script raises ModuleNotFoundError: No module named 'transformers.deepspeed'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

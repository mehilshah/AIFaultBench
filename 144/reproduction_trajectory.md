# Reproduction Trajectory — Bug 144: sentence-transformers

- **Bug report:** [https://github.com/huggingface/sentence-transformers/issues/3078](https://github.com/huggingface/sentence-transformers/issues/3078)
- **Repository:** huggingface/sentence-transformers @ `348190d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Install the requirements with ./setup_env.sh
2. Run ./run_repro.sh
3. Inspect repro_stdout.log and reproduction.json

## Observed behavior

- Constructor target device: cuda:0
- Model parameter device immediately after init: cpu
- Model.to calls after init: []
- Model.to calls after predict: ['cuda:0']
- Predict output: [0.5]
- CrossEncoder.__init__ stores the requested device but does not move the model until predict() is called.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

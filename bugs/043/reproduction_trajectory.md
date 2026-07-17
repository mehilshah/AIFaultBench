# Reproduction Trajectory — Bug 043: fairseq

- **Bug report:** [https://github.com/facebookresearch/fairseq/issues/5130](https://github.com/facebookresearch/fairseq/issues/5130)
- **Repository:** facebookresearch/fairseq @ `af12c9c6407bbcf2bca0b2f1923cf78f3db8857c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create temporary stub modules for unrelated imports so infer.py can start loading.
2. Run codebase/examples/mms/tts/infer.py from codebase/examples/mms/tts.
3. Observe ModuleNotFoundError: No module named 'commons'.

## Observed behavior

- Running examples/mms/tts/infer.py with stubbed torch/numpy modules fails immediately on 'import commons'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

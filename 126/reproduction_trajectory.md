# Reproduction Trajectory — Bug 126: codon

- **Bug report:** [https://github.com/exaloop/codon/issues/506](https://github.com/exaloop/codon/issues/506)
- **Repository:** exaloop/codon @ `32a624b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create `repro.py` containing `arr = [1, 2]` and `print(*arr)`.
2. Run `bash run_repro.sh` or equivalently `codon run repro.py`.
3. Observe the compiler error on the starred argument expansion.

## Observed behavior

- Running `codon run repro.py` with codon 0.19.6 fails at compile time with `error: argument after * must be a tuple, not 'List[int]'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

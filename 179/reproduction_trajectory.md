# Reproduction Trajectory — Bug 179: lark

- **Bug report:** [https://github.com/lark-parser/lark/issues/818](https://github.com/lark-parser/lark/issues/818)
- **Repository:** lark-parser/lark @ `9379161`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. ./setup_env.sh
2. ./run_repro.sh

## Observed behavior

- The minimal script prints `post_transform: Tree('start', [32])` and then fails on the embedded parse with `lark.exceptions.LexError: Callbacks must return a token (returned 32)`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

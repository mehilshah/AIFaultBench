# Reproduction Trajectory — Bug 177: lark

- **Bug report:** [https://github.com/lark-parser/lark/issues/1457](https://github.com/lark-parser/lark/issues/1457)
- **Repository:** lark-parser/lark @ `95e9700`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Used the bundled local `codebase/` by inserting it into `sys.path` inside `repro.py`.
2. Parsed a minimal grammar with a two-child rule so the expected inline callback signature is unambiguous.
3. Confirmed `@v_args(inline=True)` works for a `Transformer` subclass and then reproduced the mismatch on a `Visitor` subclass.

## Observed behavior

- Running `bash run_repro.sh` exits with status 1. Stdout shows the Transformer path succeeds (`transform result: 3`) and then the Visitor path begins (`visiting tree...`). Stderr ends with `TypeError: InlineVisitor.pair() missing 1 required positional argument: 'right'`, which shows `@v_args(inline=True)` is not applied to the Visitor subclass.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

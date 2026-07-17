# Reproduction Trajectory — Bug 178: lark

- **Bug report:** [https://github.com/lark-parser/lark/issues/1569](https://github.com/lark-parser/lark/issues/1569)
- **Repository:** lark-parser/lark @ `f79772c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Lark grammar with `char: /(?s)./` and `lexer="basic"`.
2. Construct `Lark(GRAMMAR, lexer="basic")` from the local `codebase/` checkout.
3. Call `list(parser.lex("\n"))` to force scanner compilation.
4. Observe the stdlib `re` crash when Lark wraps the terminal regex in a grouped alternation.

## Observed behavior

- Running `bash run_repro.sh` constructs the parser, then fails during `list(parser.lex("\n"))` with `re.error: global flags not at the start of the expression at position 13` from `codebase/lark/lexer.py` while compiling the terminal regex for `/(?s)./`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

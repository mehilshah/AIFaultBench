# Reproduction Trajectory — Bug 775: lark

- **Bug report:** [https://github.com/lark-parser/lark/issues/1570](https://github.com/lark-parser/lark/issues/1570)
- **Repository:** lark-parser/lark @ `9a4fb9c7458e8155636773a3cded0016d52516da`
- **Outcome:** Reproduced

## How the bug was reproduced

1. Cloned lark-parser/lark at the pinned commit and installed lark==1.3.1 from requirements.txt into an isolated virtualenv.
2. Built a parser from the checkout's `lark/grammars/python.lark` using the `lalr` parser and the `PythonIndenter` postlexer, matching lark's own `examples/advanced/python_parser.py` usage.
3. Parsed a non-parenthesized `with a as x, b as y:` statement to confirm the baseline grammar path works.
4. Parsed a parenthesized `with (a as x, b as y):` statement — valid Python since 3.9/3.10 and common in 3.13 code — and observed the parser reject the `as` token.

## Observed behavior

- Running `./run_repro.sh` installed lark 1.3.1, parsed the unparenthesized with-statement successfully, then failed on the parenthesized form with `Unexpected token Token('AS', 'as') at line 1, column 21`, matching the error in the original issue (`... at line 291, column 21` in the reporter's larger file).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Root cause

The `with_item` rule in `python.lark` only allows a single `test ["as" name]`:

```lark
with_stmt: "with" with_items ":" suite
with_items: with_item ("," with_item)*
with_item: test ["as" name]
```

There is no rule alternative for a parenthesized group of `with_item`s, so as soon as the lexer is inside a `(...)` group, it treats the contents as a single `test` (an expression), and the `as` keyword that follows has no valid production to attach to. As of the pinned commit, this is still unresolved upstream (`has_fix: false`).

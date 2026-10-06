# Bug 775

This folder contains a minimal reproduction bundle for:

`https://github.com/lark-parser/lark/issues/1570`

The bundled `python.lark` grammar's `with_item` rule (`test ["as" name]`)
has no alternative for a parenthesized group of context managers, so a
valid Python 3.9+/3.13 parenthesized `with` statement:

```python
with (open("a.txt") as a,
      open("b.txt") as b):
    pass
```

fails to parse with `UnexpectedToken` on the `as` keyword, while the
unparenthesized form parses fine.

Files:
- `bug_report.txt`: original issue summary
- `codebase/`: local source snapshot used for the repro
- `repro.py`: minimal reproduction using the bundled python.lark grammar
- `requirements.txt`: runtime dependencies
- `setup_env.sh`: creates the isolated environment
- `run_repro.sh`: convenience entrypoint
- `reproduction.json`: machine-readable result
- `repro_stdout.log` / `repro_stderr.log`: captured run output

Run:

`bash run_repro.sh`

# Bug 376 Reproduction

This bundle reproduces the `HFCliTyperGroup` failure reported in
`huggingface_hub==1.22.0` when Transformers CLI commands are invoked through
Typer's test runner.

## What fails

`CliRunner.invoke(transformers_cli.app, ["version"], catch_exceptions=False)`
raises:

`AttributeError: 'HFCliTyperGroup' object has no attribute '_add_completion'`

## Repro steps

1. Run `bash setup_env.sh`
2. Run `python3 repro.py`

The same flow is wrapped by `bash run_repro.sh`.

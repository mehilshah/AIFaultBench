# RoPE repro bundle

This folder reproduces the bug reported in `bug_report.txt`:

`labml_nn/transformers/rope/__init__.py` constructs `RotaryPositionalEmbeddings(3)` in the example test, but the example tensor has 4 features.

## Expected failure

Running the repro hits:

`RuntimeError: The size of tensor a (3) must match the size of tensor b (4) at non-singleton dimension 3`

## Run

```bash
bash run_repro.sh
```

The script writes:

- `repro_stdout.log`
- `repro_stderr.log`

## Notes

The corrected value is `RotaryPositionalEmbeddings(4)`, which runs successfully against the same example tensor.

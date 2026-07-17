# Bug 015 Reproduction Bundle

This folder reproduces TensorFlow Models issue 11058.

## Bug summary

The notebook helper `show_batch(raw_records, num_of_examples)` in
`codebase/docs/vision/instance_segmentation.ipynb` accepts `num_of_examples`
but never uses it inside the function body.

## Reproduction

Run:

```bash
bash run_repro.sh
```

The script writes the schema-constrained result to
`reproduction.json` and captures stdout/stderr in
`repro_stdout.log` and `repro_stderr.log`.

## What the repro checks

1. Loads the exact `show_batch` cell from the checked-in notebook.
2. Verifies that `num_of_examples` does not appear in the function body.
3. Executes the function with three records and `num_of_examples=1`.
4. Confirms the function still renders three records.

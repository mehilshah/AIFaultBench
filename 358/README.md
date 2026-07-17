# Reproduction Bundle

This bundle reproduces the `OneHotEncoding` constraint bug reported in `bug_report.txt`.

## What fails

When a table uses one-hot integer columns with metadata like:

```python
computer_representation='Int64'
```

`GaussianCopulaSynthesizer.fit()` fails after `OneHotEncoding` injects epsilon values into the
columns. The updated constraint metadata still says `Int64`, so the numerical transformer rejects
the float values.

## How to run

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro uses the local `codebase/` tree directly via `sys.path`, so no package install is needed
for the repo itself.

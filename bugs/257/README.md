# Reproduction Bundle

Bug: `SingleTableMetadata` accepts the same column as both `primary_key` and `sequence_key`.

## Repro

```bash
./setup_env.sh
./run_repro.sh
cat repro_stdout.log
cat repro_stderr.log
```

## What the repro checks

1. `metadata.validate()` with `primary_key == sequence_key`.
2. `metadata.set_sequence_key("A")` followed by `metadata.set_primary_key("A")`.

## Expected behavior

Both cases should raise `InvalidMetadataError`.

## Observed behavior

Both cases complete without error in the current local codebase.

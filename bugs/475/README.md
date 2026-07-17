# SDV issue 2768 repro

This folder contains a minimal repro for the metadata/constraint interaction reported in
`bug_report.txt`.

## What fails

`HMASynthesizer.add_constraints()` rebuilds per-table metadata from `to_dict()`. The rebuilt
`SingleTableMetadata` keeps `column_relationships` but drops the cached
`_valid_column_relationships` field. `DataProcessor._detect_multi_column_transformers()` then
dereferences that cache and raises:

`AttributeError: 'SingleTableMetadata' object has no attribute '_valid_column_relationships'`

## Reproduce

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro script uses a small bootstrap helper so it can import the local SDV snapshot without
loading optional single-table generative models that are unrelated to the bug.

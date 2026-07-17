# PyG on-disk graph loading RSS check

This bundle exercises the issue reported in `bug_report.txt` using a clean
Python environment and the reported PyG release line.

## What it does

- Creates a dataset that saves graphs to disk on first access.
- Loads those graphs through `torch_geometric.loader.DataLoader`.
- Prints process RSS before the loop and after each epoch.

## Expected command

```bash
bash run_repro.sh
```

## Result in this folder

The reproduction was **not** observed here. RSS rose during warmup, then
fluctuated in a bounded range instead of increasing every epoch.

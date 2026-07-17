# Reproduction Bundle

This folder reproduces the reported diagonal-pattern behavior in `einops`.

## What it shows

`rearrange` and `reduce` reject repeated axis names such as:

* `rearrange(matrix, "ii->i")`
* `rearrange(tensor, "iii->i")`
* `rearrange(vector, "i->ii")`
* `reduce(matrix, "ii->i", "sum")`
* `reduce(matrix, "ii->i", "max")`

The current checkout raises `EinopsError` with a duplicate-dimension message for each case.

## Setup

```bash
bash setup_env.sh
```

This creates a local `.venv/` in the folder and installs the minimal dependency set into it.

## Run

```bash
bash run_repro.sh
```


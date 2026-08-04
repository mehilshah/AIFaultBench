#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/patrick-kidger/jaxtyping codebase
git -C codebase checkout c2f19dbea305e1e3b0b1d259ce56ee433a2df9e5
# then: bash setup_env.sh && bash run_repro.sh

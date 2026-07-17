#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout fae65964d712b1c93d620e23237a18b2f3ffaa9e
# then: bash setup_env.sh && bash run_repro.sh

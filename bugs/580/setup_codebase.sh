#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout ab2b458f0c0f72d3cb573350b324db563066a7ee
# then: bash setup_env.sh && bash run_repro.sh

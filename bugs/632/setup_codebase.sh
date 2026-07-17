#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout 46705844b39ededc0fcef1de90e73923480a6446
# then: bash setup_env.sh && bash run_repro.sh

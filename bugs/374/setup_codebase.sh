#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout a0f9e8fe469ef50760ae0c9a2702bf8443017b0c
# then: bash setup_env.sh && bash run_repro.sh

#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout 44dee49ad88cf5253e8092cfce3e453c00bc8c3e
# then: bash setup_env.sh && bash run_repro.sh

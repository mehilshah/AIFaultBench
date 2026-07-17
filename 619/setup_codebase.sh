#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout bd5ae45c74a3fbb6b6ff818476f7651d84313d2a
# then: bash setup_env.sh && bash run_repro.sh

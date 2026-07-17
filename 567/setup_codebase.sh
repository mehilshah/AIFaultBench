#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout ef028547ff4459f6e98fe429d1564bd1d513fc31
# then: bash setup_env.sh && bash run_repro.sh

#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout 47ac8186010bcd14ce14493f02075962d6b359d5
# then: bash setup_env.sh && bash run_repro.sh

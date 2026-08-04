#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout e167d2bfd438935e7fee35236c15c8952889e95a
# then: bash setup_env.sh && bash run_repro.sh

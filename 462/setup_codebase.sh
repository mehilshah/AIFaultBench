#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout afffee9f089ac0fe1eb8c1600c6e0b2e07ca6f80
# then: bash setup_env.sh && bash run_repro.sh

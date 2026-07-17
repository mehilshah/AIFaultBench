#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout 5fb2a8eaae3047a9dd430fd58e735e333daed79d
# then: bash setup_env.sh && bash run_repro.sh

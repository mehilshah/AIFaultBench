#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/meta-pytorch/torchtune codebase
git -C codebase checkout 2344509cf83bd886538fe3e8263e5145d1afb5c2
# then: bash setup_env.sh && bash run_repro.sh

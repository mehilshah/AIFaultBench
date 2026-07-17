#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/fairseq codebase
git -C codebase checkout 1082b61b12ec92d6c813906fcec90139b85fb039
# then: bash setup_env.sh && bash run_repro.sh

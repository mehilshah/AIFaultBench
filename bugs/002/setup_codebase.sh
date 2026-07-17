#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout 1bdb87d92d40e8f63285dafb6803139e25a59baf
# then: bash setup_env.sh && bash run_repro.sh

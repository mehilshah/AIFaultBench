#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/kubeflow/katib codebase
git -C codebase checkout 87aec69b9f5d62be29d22a7744bf2cf581b45104
# then: bash setup_env.sh && bash run_repro.sh

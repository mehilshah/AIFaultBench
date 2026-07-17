#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout d63c8e944481e057d00dfee20bc49544d291e521
# then: bash setup_env.sh && bash run_repro.sh

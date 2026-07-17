#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout 5274c1181dc61bdf6e5eb610d37ebef694b1340d
# then: bash setup_env.sh && bash run_repro.sh

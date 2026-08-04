#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Trusted-AI/adversarial-robustness-toolbox codebase
git -C codebase checkout a5a61d3761edfa71c645c652d30f212308c4a8c9
# then: bash setup_env.sh && bash run_repro.sh

#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/stanfordnlp/dspy codebase
git -C codebase checkout e842ba176a7183061815946cd3adcedd1dae8126
# then: bash setup_env.sh && bash run_repro.sh

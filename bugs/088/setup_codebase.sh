#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/x-transformers codebase
git -C codebase checkout 144d9ba84955139347e798ab025457b2d7adc314
# then: bash setup_env.sh && bash run_repro.sh

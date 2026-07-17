#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/x-transformers codebase
git -C codebase checkout 6db4d225fb3fb95cbdb480bdec0a71313f2666f0
# then: bash setup_env.sh && bash run_repro.sh

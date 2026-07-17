#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/x-transformers codebase
git -C codebase checkout 43960ad12ac2eb3c943688430ec58fa8e82752e7
# then: bash setup_env.sh && bash run_repro.sh

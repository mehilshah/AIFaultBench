#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/x-transformers codebase
git -C codebase checkout 57efd7770f2f5df0ff7b4ffcbd623750b584e850
# then: bash setup_env.sh && bash run_repro.sh

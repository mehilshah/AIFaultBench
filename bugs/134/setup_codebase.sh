#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/flairNLP/flair codebase
git -C codebase checkout d4ea3777998ba67bfbe6b6b8359e024dcf673c3e
# then: bash setup_env.sh && bash run_repro.sh

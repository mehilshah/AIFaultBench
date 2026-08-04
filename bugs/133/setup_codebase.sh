#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/flairNLP/flair codebase
git -C codebase checkout ee8596c2bbe737ec9ddeb1c6cb62fa0b161f4d84
# then: bash setup_env.sh && bash run_repro.sh

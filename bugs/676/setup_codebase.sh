#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/stanfordnlp/dspy codebase
git -C codebase checkout d27c5afe5e5f027a9b23e7f9e33ede3160edf28f
# then: bash setup_env.sh && bash run_repro.sh

#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/stanfordnlp/dspy codebase
git -C codebase checkout da69f9d05fc7509eb20c4acb41e8b8b793104f7e
# then: bash setup_env.sh && bash run_repro.sh

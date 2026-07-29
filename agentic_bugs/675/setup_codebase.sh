#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/stanfordnlp/dspy codebase
git -C codebase checkout fd93c38ca0548beaf512d6e4c3506c04d291cdb4
# then: bash setup_env.sh && bash run_repro.sh

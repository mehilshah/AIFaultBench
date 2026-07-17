#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/labmlai/annotated_deep_learning_paper_implementations codebase
git -C codebase checkout 732aedcfc664d032f3a9b90c623e1dbe9ef3fba9
# then: bash setup_env.sh && bash run_repro.sh

#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout e923b8aa3b066c02432ffdb7d5fd93d465b6eaa5
# then: bash setup_env.sh && bash run_repro.sh

#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/stanfordnlp/dspy codebase
git -C codebase checkout ba32809e730d9c35969a4d899fde0305344638a1
# then: bash setup_env.sh && bash run_repro.sh

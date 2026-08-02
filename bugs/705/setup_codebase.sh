#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/stanfordnlp/dspy codebase
git -C codebase checkout c542bb64a7bb321fe16fd159a5da646ca4d92974
# then: bash setup_env.sh && bash run_repro.sh

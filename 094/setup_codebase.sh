#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/PaLM-rlhf-pytorch codebase
git -C codebase checkout e624afd8860d6df8f7a429dbe518a2fd40b4cc34
# then: bash setup_env.sh && bash run_repro.sh

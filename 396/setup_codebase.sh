#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/peft codebase
git -C codebase checkout 30fd5a4c88db369e87eab27ebf01c0b28bed02dc
# then: bash setup_env.sh && bash run_repro.sh

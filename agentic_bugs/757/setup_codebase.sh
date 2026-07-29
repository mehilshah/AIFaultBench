#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/smolagents codebase
git -C codebase checkout c035a10e991408f2ccf49fe1cfcfaf0d9a34b011
# then: bash setup_env.sh && bash run_repro.sh

#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/mem0ai/mem0 codebase
git -C codebase checkout f38608fb5061c5aa067793740447cf217b3afee0
# then: bash setup_env.sh && bash run_repro.sh

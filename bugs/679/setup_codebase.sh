#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/camel-ai/camel codebase
git -C codebase checkout eed7320daa44f42470c6cb7347db1e06b72d9c39
# then: bash setup_env.sh && bash run_repro.sh

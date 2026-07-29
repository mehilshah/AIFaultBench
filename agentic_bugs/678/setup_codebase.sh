#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/camel-ai/camel codebase
git -C codebase checkout d84c72c78259b5c7358fa92e1f280e85e2e39f56
# then: bash setup_env.sh && bash run_repro.sh

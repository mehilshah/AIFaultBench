#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/camel-ai/camel codebase
git -C codebase checkout c7d4423ac566a89d8e509146187399e28832bf24
# then: bash setup_env.sh && bash run_repro.sh

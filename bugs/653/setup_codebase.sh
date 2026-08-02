#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/camel-ai/camel codebase
git -C codebase checkout 526578ee04bd2f9e32843534067df97f8c445594
# then: bash setup_env.sh && bash run_repro.sh

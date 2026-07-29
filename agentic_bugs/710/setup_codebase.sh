#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/camel-ai/camel codebase
git -C codebase checkout e5883ec426afa9d2398f9c82d274ebed4cd25e98
# then: bash setup_env.sh && bash run_repro.sh

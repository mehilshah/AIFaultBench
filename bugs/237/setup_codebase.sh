#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/patrick-kidger/jaxtyping codebase
git -C codebase checkout f4ca4c98fecf9bf1d85c727e40bf1630a190a70f
# then: bash setup_env.sh && bash run_repro.sh

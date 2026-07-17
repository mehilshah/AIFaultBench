#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-io codebase
git -C codebase checkout af2817346c38effe497db8a771c5eb65f1e46144
# then: bash setup_env.sh && bash run_repro.sh

#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/thu-ml/tianshou codebase
git -C codebase checkout be657fa753e3d1572318d7bbf9adb8e2bf1c7f43
# then: bash setup_env.sh && bash run_repro.sh

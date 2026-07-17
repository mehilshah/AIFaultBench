#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout 272c3fab3557a09d4fa4260418836f74d7c4a503
# then: bash setup_env.sh && bash run_repro.sh

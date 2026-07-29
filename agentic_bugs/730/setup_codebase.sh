#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/semantic-kernel codebase
git -C codebase checkout 28ea2f4df872e8fd03ef0792ebc9e1989b4be0ee
# then: bash setup_env.sh && bash run_repro.sh

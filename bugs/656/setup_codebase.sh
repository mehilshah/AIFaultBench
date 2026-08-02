#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/browser-use/browser-use codebase
git -C codebase checkout 5882675788972894be68baa53c8a1d80e9815c3e
# then: bash setup_env.sh && bash run_repro.sh

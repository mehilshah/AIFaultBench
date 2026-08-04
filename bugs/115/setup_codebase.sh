#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/axolotl-ai-cloud/axolotl codebase
git -C codebase checkout c10eb811fac677ee2d7c0c38a44d084fcc613cdc
# then: bash setup_env.sh && bash run_repro.sh

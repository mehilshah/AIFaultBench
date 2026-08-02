#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/SWE-agent/SWE-agent codebase
git -C codebase checkout b21a0614da892c758ca15ab91f759caa147f09e4
# then: bash setup_env.sh && bash run_repro.sh

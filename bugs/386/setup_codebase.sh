#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout 01ccf3647c1c1031b8a188488f1330b16fb5fd31
# then: bash setup_env.sh && bash run_repro.sh

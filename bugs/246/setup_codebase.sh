#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout 0678b357ee6184c6dbaedaa500ea28569b4dd6e5
# then: bash setup_env.sh && bash run_repro.sh

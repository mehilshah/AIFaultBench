#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout 0c7884dd6c06a8457a0696126f32d7ce7f404945
# then: bash setup_env.sh && bash run_repro.sh

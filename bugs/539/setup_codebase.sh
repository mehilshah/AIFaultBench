#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout f4fafc5c7fa0dc5a377ceb06ec59a234bf3ac465
# then: bash setup_env.sh && bash run_repro.sh

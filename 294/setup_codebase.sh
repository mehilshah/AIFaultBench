#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout ca36025a3502c0160395b53145d2e95b56eaf15f
# then: bash setup_env.sh && bash run_repro.sh

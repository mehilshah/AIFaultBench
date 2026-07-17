#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout dd4e0f81b4ddceb82ebd663b20333e175ce27c2a
# then: bash setup_env.sh && bash run_repro.sh

#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout 005032f10099188fea86f63b6baa46a27867983f
# then: bash setup_env.sh && bash run_repro.sh

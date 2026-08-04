#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/torchtitan codebase
git -C codebase checkout cd337db6303870a4182a730d1c4d6941f47bb2b8
# then: bash setup_env.sh && bash run_repro.sh

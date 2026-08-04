#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 36545af5062821dada2cdb91594209442d3dd0e6
# then: bash setup_env.sh && bash run_repro.sh

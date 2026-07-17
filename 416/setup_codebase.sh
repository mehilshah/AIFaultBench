#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout b8e0c3ce78b420c7484d3761791f832b988b3a02
# then: bash setup_env.sh && bash run_repro.sh

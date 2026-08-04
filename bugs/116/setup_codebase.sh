#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/bayesflow-org/bayesflow codebase
git -C codebase checkout a4d58c90b5ea9a98a928bdfe722c01477a95dff3
# then: bash setup_env.sh && bash run_repro.sh

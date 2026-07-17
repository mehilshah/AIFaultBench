#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout a14fabc980ef115f499c89ffb242cbba8555e824
# then: bash setup_env.sh && bash run_repro.sh

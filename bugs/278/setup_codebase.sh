#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout bfe88ed8f000b88a546dc1c8848ecf5905082df2
# then: bash setup_env.sh && bash run_repro.sh

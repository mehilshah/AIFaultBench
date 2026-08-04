#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout d28fd826aa7f3c6f4f475761ca53989ca4bc84a7
# then: bash setup_env.sh && bash run_repro.sh

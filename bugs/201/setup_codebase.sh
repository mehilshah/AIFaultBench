#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout 9ce2384595975cd7a1b9a51402124c999ee0141a
# then: bash setup_env.sh && bash run_repro.sh

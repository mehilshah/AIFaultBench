#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout ff6f5675249d6192e1f8613f8b073f70c8898ba2
# then: bash setup_env.sh && bash run_repro.sh

#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout 68d86dc0535c5488f497790af2305d19d74d924a
# then: bash setup_env.sh && bash run_repro.sh

#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout 43fa32ce00c293367ebafbfc4a047840906dcb8b
# then: bash setup_env.sh && bash run_repro.sh

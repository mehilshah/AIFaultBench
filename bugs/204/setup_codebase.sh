#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout fb14da77654035cefd438c86062c24db8eb3befe
# then: bash setup_env.sh && bash run_repro.sh

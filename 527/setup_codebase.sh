#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout a98bb57e1704997a3e01c76a7820c0b1db909ee3
# then: bash setup_env.sh && bash run_repro.sh

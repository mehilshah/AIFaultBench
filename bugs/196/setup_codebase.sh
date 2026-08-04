#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/patrick-kidger/jaxtyping codebase
git -C codebase checkout bd84aed3e59492e0275a2cda854627cb50d75f48
# then: bash setup_env.sh && bash run_repro.sh

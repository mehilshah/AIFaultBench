#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 05aa8a8029e989a6091ff1b14a60892d194397fb
# then: bash setup_env.sh && bash run_repro.sh

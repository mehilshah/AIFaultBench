#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 9354783e3dc41f69b252992c8dd6526a3ad981f2
# then: bash setup_env.sh && bash run_repro.sh

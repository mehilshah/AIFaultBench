#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 0063741839a3e5e1a527947945494d54f91bc629
# then: bash setup_env.sh && bash run_repro.sh

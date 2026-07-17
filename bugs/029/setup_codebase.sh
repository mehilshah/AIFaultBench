#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/examples codebase
git -C codebase checkout 54f4572509891883a947411fd7239237dd2a39c3
# then: bash setup_env.sh && bash run_repro.sh

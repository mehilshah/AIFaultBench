#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/SWE-agent/SWE-agent codebase
git -C codebase checkout ec75580fe90f198bce2730e3642f33f5874f3357
# then: bash setup_env.sh && bash run_repro.sh

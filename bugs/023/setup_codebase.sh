#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout e871d4739e89bcc2b6b16c8e8a8d3eea3eaf1bae
# then: bash setup_env.sh && bash run_repro.sh

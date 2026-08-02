#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/stanfordnlp/dspy codebase
git -C codebase checkout 9cdb0aac28b2a04b064e40697ccd301872cf6a43
# then: bash setup_env.sh && bash run_repro.sh

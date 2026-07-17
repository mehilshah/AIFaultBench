#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/stanfordnlp/stanza codebase
# then: bash setup_env.sh && bash run_repro.sh

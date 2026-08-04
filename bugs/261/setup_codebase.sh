#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/stanfordnlp/stanza codebase
git -C codebase checkout d29896f2705368b74a81d6cb0dc7facda4b3e732
# then: bash setup_env.sh && bash run_repro.sh

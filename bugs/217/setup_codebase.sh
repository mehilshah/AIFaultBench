#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/stanfordnlp/stanza codebase
git -C codebase checkout 17eb6fc2bfd45bd5f36135219ccc527cd7065366
# then: bash setup_env.sh && bash run_repro.sh

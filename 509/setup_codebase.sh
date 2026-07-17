#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout aab99f8a693943a95fb3380838bb6b56e77e677e
# then: bash setup_env.sh && bash run_repro.sh

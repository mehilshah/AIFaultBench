#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/PythonOT/POT codebase
git -C codebase checkout a29e22db4772ebc4a8266c917e2e662f624c6baa
# then: bash setup_env.sh && bash run_repro.sh

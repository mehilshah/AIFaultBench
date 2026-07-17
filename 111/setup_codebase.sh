#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/ahmedfgad/GeneticAlgorithmPython codebase
git -C codebase checkout 9ac7527
# then: bash setup_env.sh && bash run_repro.sh

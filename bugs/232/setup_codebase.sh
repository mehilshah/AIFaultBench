#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/ourownstory/neural_prophet codebase
git -C codebase checkout 23543560b4ed278e84d1fd0f119d332342336d0d
# then: bash setup_env.sh && bash run_repro.sh

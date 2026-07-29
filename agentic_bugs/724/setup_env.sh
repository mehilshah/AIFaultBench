#!/usr/bin/env bash
set -euo pipefail

task_venv=".venv"
python3 -m venv "$task_venv"
"$task_venv/bin/python" -m pip install --upgrade pip
"$task_venv/bin/python" -m pip install -r requirements.txt
"$task_venv/bin/python" -m pip install --no-deps -e codebase/lib/crewai

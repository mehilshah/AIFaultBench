#!/usr/bin/env bash
set -euo pipefail

python3.11 -m pip install --upgrade pip
python3.11 -m pip install --break-system-packages -r requirements.txt

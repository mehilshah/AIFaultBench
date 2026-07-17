#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 -m pip install --user --break-system-packages --disable-pip-version-check -r requirements.txt

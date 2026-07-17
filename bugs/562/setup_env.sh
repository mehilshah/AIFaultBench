#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --upgrade \
  torch==2.3.1+cpu torchvision==0.18.1+cpu \
  --index-url https://download.pytorch.org/whl/cpu \
  --extra-index-url https://pypi.org/simple
python -m pip install -r requirements.txt

export PYTHONPATH="$(pwd)/codebase:${PYTHONPATH:-}"
echo "PYTHONPATH=$PYTHONPATH"

#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade --force-reinstall \
  torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 \
  --index-url https://download.pytorch.org/whl/cu121
python3 -m pip install -r requirements.txt
python3 -m pip install --upgrade \
  torch-scatter==2.1.2 torch-sparse==0.6.18 \
  -f https://data.pyg.org/whl/torch-2.5.1+cu121.html

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

python3 -m venv .venv_repro
source .venv_repro/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install --index-url https://download.pytorch.org/whl/cpu 'torch==2.3.1+cpu'
python -m pip install --no-deps 'transformers==4.44.2' 'accelerate==0.33.0' 'tokenizers==0.19.1' 'huggingface_hub==0.36.2' 'safetensors==0.8.0' 'numpy==1.26.4' 'pyyaml==6.0.3' 'regex==2026.7.10' 'requests==2.34.2' 'tqdm==4.68.4' 'filelock==3.30.2' 'psutil==7.2.2' 'typing_extensions==4.16.0' 'hf-xet==1.5.2'
python -m pip install 'urllib3==2.7.0' 'certifi==2026.6.17' 'charset_normalizer==3.4.9' 'idna==3.18' 'packaging==26.2'

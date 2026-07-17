#!/usr/bin/env bash
set -euo pipefail

source .venv/bin/activate
NCCL_P2P_LEVEL=LOC accelerate launch --config_file fsdp2.yaml repro.py

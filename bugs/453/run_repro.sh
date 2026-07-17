#!/usr/bin/env bash
set -euo pipefail

export PATH="$PWD/.venv/bin:$PATH"
export NCCL_DEBUG="${NCCL_DEBUG:-WARN}"
export TORCH_DISTRIBUTED_DEBUG="${TORCH_DISTRIBUTED_DEBUG:-DETAIL}"
export DEEPSPEED_CONFIG="${DEEPSPEED_CONFIG:-ds_config_zero3_stress.json}"
export VOCAB="${VOCAB:-32768}"
export D_MODEL="${D_MODEL:-2048}"
export ITERS="${ITERS:-200}"
export TILE="${TILE:-8}"
export DO_BWD="${DO_BWD:-1}"
export FORCE_GATHER_EDIT="${FORCE_GATHER_EDIT:-1}"
export NPROC_PER_NODE="${NPROC_PER_NODE:-2}"

exec .venv/bin/torchrun --standalone --nproc_per_node="${NPROC_PER_NODE}" repro.py

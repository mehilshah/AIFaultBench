#!/bin/sh
set -eu

sh ./setup_env.sh
.venv/bin/python repro.py

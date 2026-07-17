#!/usr/bin/env bash
set -euo pipefail

python3 -W ignore::DeprecationWarning repro.py

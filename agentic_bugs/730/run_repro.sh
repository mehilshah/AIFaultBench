#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ ! -x "$repo_root/.venv/bin/python" || ! -x "$repo_root/.venv/dotnet/usr/lib/dotnet/dotnet" ]]; then
    bash "$repo_root/setup_env.sh"
fi
exec "$repo_root/.venv/bin/python" "$repo_root/repro.py"

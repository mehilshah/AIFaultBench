#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -d "$repo_root/.venv" || ! -x "$repo_root/.venv/dotnet/dotnet" || ! -f "$repo_root/.venv/repro-project/obj/project.assets.json" ]]; then
  bash "$repo_root/setup_env.sh"
fi

exec "$repo_root/.venv/bin/python" "$repo_root/repro.py"

#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
venv_root="$repo_root/.venv"
dotnet_root="$venv_root/dotnet"
dotnet_bin="$dotnet_root/usr/lib/dotnet/dotnet"

python3 -m venv "$venv_root"
"$venv_root/bin/python" -m pip install --disable-pip-version-check -r "$repo_root/requirements.txt"

if [[ ! -x "$dotnet_bin" ]]; then
    package_dir="$(mktemp -d)"
    trap 'rm -rf "$package_dir"' EXIT
    (
        cd "$package_dir"
        apt-get download \
            aspnetcore-runtime-8.0=8.0.29-0ubuntu1~24.04.1 \
            aspnetcore-targeting-pack-8.0=8.0.29-0ubuntu1~24.04.1 \
            dotnet-apphost-pack-8.0=8.0.29-0ubuntu1~24.04.1 \
            dotnet-host-8.0=8.0.29-0ubuntu1~24.04.1 \
            dotnet-hostfxr-8.0=8.0.29-0ubuntu1~24.04.1 \
            dotnet-runtime-8.0=8.0.29-0ubuntu1~24.04.1 \
            dotnet-sdk-8.0=8.0.129-0ubuntu1~24.04.1 \
            dotnet-targeting-pack-8.0=8.0.29-0ubuntu1~24.04.1 \
            dotnet-templates-8.0=8.0.129-0ubuntu1~24.04.1 \
            netstandard-targeting-pack-2.1-8.0=8.0.129-0ubuntu1~24.04.1
        for package_file in ./*.deb; do
            dpkg-deb -x "$package_file" "$dotnet_root"
        done
    )
fi

"$venv_root/bin/python" "$repo_root/repro.py" --restore-only

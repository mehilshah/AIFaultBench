#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
venv_dir="$repo_root/.venv"
dotnet_dir="$venv_dir/dotnet"
project_dir="$venv_dir/repro-project"
project_file="$project_dir/Repro.csproj"

python3 -m venv "$venv_dir"
"$venv_dir/bin/python" -m pip install --disable-pip-version-check -r "$repo_root/requirements.txt"

if [[ ! -x "$dotnet_dir/dotnet" ]]; then
  curl --fail --location --silent --show-error https://dot.net/v1/dotnet-install.sh \
    --output "$venv_dir/dotnet-install.sh"
  bash "$venv_dir/dotnet-install.sh" --version 10.0.100 --install-dir "$dotnet_dir" --no-path
fi

mkdir -p "$project_dir"
cat > "$project_file" <<'EOF'
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net48</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <LangVersion>latest</LangVersion>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.SemanticKernel.Connectors.InMemory" Version="1.66.0-preview" />
    <PackageReference Include="Microsoft.NETFramework.ReferenceAssemblies" Version="1.0.3" PrivateAssets="all" />
  </ItemGroup>
</Project>
EOF

cat > "$project_dir/Program.cs" <<'EOF'
internal static class Program
{
    private static void Main() { }
}
EOF

export DOTNET_CLI_HOME="$venv_dir/dotnet-home"
export DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1
export NUGET_PACKAGES="$venv_dir/nuget"
"$dotnet_dir/dotnet" restore "$project_file" --verbosity minimal

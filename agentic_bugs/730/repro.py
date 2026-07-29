#!/usr/bin/env python3
"""Offline reproduction for semantic-kernel issue #13148."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DOTNET = ROOT / ".venv" / "dotnet" / "usr" / "lib" / "dotnet" / "dotnet"
CONNECTOR = ROOT / "codebase" / "dotnet" / "src" / "Connectors" / "Connectors.HuggingFace" / "Connectors.HuggingFace.csproj"
NUGET_CONFIG = ROOT / "codebase" / "dotnet" / "nuget.config"

PROGRAM = r'''using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.AI;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.HuggingFace;

sealed class Recording404Handler : HttpMessageHandler
{
    public Uri? RequestUri { get; private set; }

    protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
    {
        RequestUri = request.RequestUri;
        return Task.FromResult(new HttpResponseMessage(HttpStatusCode.NotFound)
        {
            Content = new StringContent("offline Hugging Face stub: endpoint not found")
        });
    }
}

static class Program
{
    static async Task<int> Main()
    {
        const string model = "sentence-transformers/all-MiniLM-L6-v2";
        const string obsoleteEndpoint =
            "https://api-inference.huggingface.co/pipeline/feature-extraction/" + model;

        var handler = new Recording404Handler();
        using var httpClient = new HttpClient(handler);
        var builder = Kernel.CreateBuilder();
        builder.AddHuggingFaceEmbeddingGenerator(model, apiKey: "unused-offline-key", httpClient: httpClient);
        var kernel = builder.Build();
        var generator = kernel.GetRequiredService<IEmbeddingGenerator<string, Embedding<float>>>();

        try
        {
            await generator.GenerateAsync(new[] { "John: Hello, how are you?\nRoger: Hey, I'm Roger!" });
            throw new InvalidOperationException("The local 404 stub should have caused HttpOperationException.");
        }
        catch (HttpOperationException error) when (
            error.StatusCode == HttpStatusCode.NotFound &&
            handler.RequestUri?.AbsoluteUri == obsoleteEndpoint)
        {
            Console.WriteLine($"OBSERVED_BUG: HttpOperationException 404 after request to {handler.RequestUri!.AbsoluteUri}");
            return 1;
        }
    }
}
'''


def main() -> int:
    if not DOTNET.is_file():
        raise RuntimeError(f"Missing isolated .NET SDK at {DOTNET}; run bash setup_env.sh first.")
    if not CONNECTOR.is_file():
        raise RuntimeError("Missing pinned checkout; run bash setup_codebase.sh first.")

    environment = os.environ.copy()
    environment["DOTNET_CLI_HOME"] = str(ROOT / ".venv" / "dotnet-cli")
    environment["NUGET_PACKAGES"] = str(ROOT / ".venv" / "nuget")

    project_dir = ROOT / ".venv" / "repro-build"
    project_dir.mkdir(exist_ok=True)
    (project_dir / "Program.cs").write_text(PROGRAM, encoding="utf-8")
    (project_dir / "Repro.csproj").write_text(
        "<Project Sdk=\"Microsoft.NET.Sdk\">\n"
        "  <PropertyGroup><OutputType>Exe</OutputType><TargetFramework>net8.0</TargetFramework>"
        "<ImplicitUsings>disable</ImplicitUsings><Nullable>enable</Nullable></PropertyGroup>\n"
        f"  <ItemGroup><ProjectReference Include=\"{CONNECTOR}\" /></ItemGroup>\n"
        "</Project>\n",
        encoding="utf-8",
    )

    if sys.argv[1:] == ["--restore-only"]:
        command = [str(DOTNET), "restore", "Repro.csproj", "--configfile", str(NUGET_CONFIG), "--nologo"]
    elif not sys.argv[1:]:
        command = [str(DOTNET), "run", "--no-restore", "--project", "Repro.csproj", "--nologo"]
    else:
        raise RuntimeError("usage: repro.py [--restore-only]")

    return subprocess.run(command, cwd=project_dir, env=environment, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())

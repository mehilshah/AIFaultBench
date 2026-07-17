#!/usr/bin/env python3
"""Minimal reproduction for the Docker version JSON schema mismatch."""

from __future__ import annotations

import json
import sys
from pathlib import Path
import traceback

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

import cibuildwheel.oci_container as oci_container
from cibuildwheel.errors import OCIEngineTooOldError
from cibuildwheel.oci_container import OCIContainerEngineConfig, _check_engine_version


BUGGY_DOCKER_VERSION_JSON = {
    "Client": {
        "Platform": {"Name": "Docker Engine - Community"},
        "Version": "29.0.0",
        "ApiVersion": "1.52",
        "DefaultAPIVersion": "1.52",
        "GitCommit": "3d4129b",
        "GoVersion": "go1.25.4",
        "Os": "linux",
        "Arch": "amd64",
        "BuildTime": "Mon Nov 10 21:46:28 2025",
        "Context": "default",
    },
    "Server": {
        "Platform": {"Name": "Docker Engine - Community"},
        "Version": "29.0.0",
        "APIVersion": "1.52",
        "MinAPIVersion": "1.44",
        "Os": "linux",
        "Arch": "amd64",
        "Experimental": False,
        "Components": [
            {
                "Name": "Engine",
                "Version": "29.0.0",
                "Details": {
                    "ApiVersion": "1.52",
                    "Arch": "amd64",
                    "BuildTime": "Mon Nov 10 21:47:52 2025",
                    "Experimental": "false",
                    "GitCommit": "d105562",
                    "GoVersion": "go1.25.4",
                    "KernelVersion": "5.15.154+",
                    "MinAPIVersion": "1.44",
                    "Os": "linux",
                },
            },
            {
                "Name": "containerd",
                "Version": "v2.1.5",
                "Details": {"GitCommit": "fcd43222d6b07379a4be9786bda52438f0dd16a1"},
            },
            {
                "Name": "runc",
                "Version": "1.3.3",
                "Details": {"GitCommit": "v1.3.3-0-gd842d77"},
            },
            {
                "Name": "docker-init",
                "Version": "0.19.0",
                "Details": {"GitCommit": "de40ad0"},
            },
        ],
    },
}


def main() -> int:
    def fake_call(*args, **kwargs):
        return json.dumps(BUGGY_DOCKER_VERSION_JSON)

    oci_container.call = fake_call
    engine = OCIContainerEngineConfig.from_config_string("docker")

    try:
        _check_engine_version(engine)
    except OCIEngineTooOldError as exc:
        print("OCIEngineTooOldError raised")
        print(exc)
        if exc.__cause__ is not None:
            print(f"cause: {type(exc.__cause__).__name__}: {exc.__cause__}")
        traceback.print_exception(type(exc), exc, exc.__traceback__)
        return 1

    print("unexpected success")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

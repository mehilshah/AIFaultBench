#!/usr/bin/env python3
"""Reproduce the DeepVariant 1.6.1 container version mismatch.

This checks the Docker Hub image metadata for google/deepvariant:1.6.1 and
verifies the image config still advertises VERSION=1.6.0.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request


DEFAULT_REPO = "google/deepvariant"
DEFAULT_TAG = "1.6.1"
EXPECTED_VERSION = "1.6.1"


def fetch_json(url: str, headers: dict[str, str] | None = None) -> dict:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def get_bearer_token(repo: str) -> str:
    scope = f"repository:{repo}:pull"
    params = urllib.parse.urlencode(
        {"service": "registry.docker.io", "scope": scope}
    )
    data = fetch_json(f"https://auth.docker.io/token?{params}")
    return data["token"]


def fetch_manifest(repo: str, tag: str, token: str) -> tuple[dict, str | None]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": ",".join(
            [
                "application/vnd.docker.distribution.manifest.v2+json",
                "application/vnd.oci.image.manifest.v1+json",
                "application/vnd.docker.distribution.manifest.list.v2+json",
                "application/vnd.oci.image.index.v1+json",
            ]
        ),
    }
    req = urllib.request.Request(
        f"https://registry-1.docker.io/v2/{repo}/manifests/{tag}", headers=headers
    )
    with urllib.request.urlopen(req) as resp:
        content_type = resp.headers.get("Content-Type")
        manifest = json.load(resp)
    return manifest, content_type


def select_manifest_digest(manifest: dict) -> str | None:
    if "config" in manifest:
        return manifest["config"]["digest"]
    for entry in manifest.get("manifests", []):
        platform = entry.get("platform", {})
        if platform.get("os") == "linux" and platform.get("architecture") == "amd64":
            return entry["digest"]
    return None


def fetch_config(repo: str, digest: str, token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    return fetch_json(f"https://registry-1.docker.io/v2/{repo}/blobs/{digest}", headers)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--tag", default=DEFAULT_TAG)
    parser.add_argument("--expected-version", default=EXPECTED_VERSION)
    args = parser.parse_args()

    print(f"Inspecting {args.repo}:{args.tag}")
    token = get_bearer_token(args.repo)
    manifest, content_type = fetch_manifest(args.repo, args.tag, token)
    print(f"Manifest content-type: {content_type}")

    digest = select_manifest_digest(manifest)
    if not digest:
        print("Unable to select a config digest from the manifest.", file=sys.stderr)
        return 2

    if "config" not in manifest:
        print(f"Selected platform manifest digest: {digest}")
        manifest = fetch_json(
            f"https://registry-1.docker.io/v2/{args.repo}/manifests/{digest}",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": ",".join(
                    [
                        "application/vnd.docker.distribution.manifest.v2+json",
                        "application/vnd.oci.image.manifest.v1+json",
                    ]
                ),
            },
        )
        digest = manifest["config"]["digest"]

    print(f"Config digest: {digest}")
    config = fetch_config(args.repo, digest, token)
    env = config.get("config", {}).get("Env", [])
    version = next((item.split("=", 1)[1] for item in env if item.startswith("VERSION=")), None)

    print(f"Image VERSION env: {version}")
    print(f"Expected VERSION: {args.expected_version}")

    if version != args.expected_version:
        print(
            f"Mismatch reproduced: {args.repo}:{args.tag} advertises VERSION={version}",
            file=sys.stderr,
        )
        return 1

    print("No mismatch found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

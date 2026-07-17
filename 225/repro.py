#!/usr/bin/env python3
"""Minimal reproduction for the JWT auth bypass in deploy/docker/auth.py."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parent
AUTH_DIR = ROOT / "codebase" / "deploy" / "docker"
sys.path.insert(0, str(AUTH_DIR))

from auth import create_access_token, get_token_dependency  # noqa: E402


CONFIG = {"security": {"jwt_enabled": True}}
TOKEN_DEP = get_token_dependency(CONFIG)

app = FastAPI()


@app.get("/protected")
async def protected(_td: dict = Depends(TOKEN_DEP)):
    return {"success": True, "dependency_value": _td}


def main() -> int:
    client = TestClient(app)

    no_token_response = client.get("/protected")
    invalid_token_response = client.get(
        "/protected",
        headers={"Authorization": "Bearer definitely-not-a-real-token"},
    )
    valid_token = create_access_token({"sub": "test@example.com"})
    valid_token_response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    report = {
        "no_token": {
            "status_code": no_token_response.status_code,
            "body": no_token_response.json(),
        },
        "invalid_token": {
            "status_code": invalid_token_response.status_code,
            "body": invalid_token_response.json(),
        },
        "valid_token": {
            "status_code": valid_token_response.status_code,
            "body": valid_token_response.json(),
        },
    }

    print(json.dumps(report, indent=2, sort_keys=True))

    reproduced = no_token_response.status_code == 200 and invalid_token_response.status_code == 401
    return 0 if reproduced else 1


if __name__ == "__main__":
    raise SystemExit(main())

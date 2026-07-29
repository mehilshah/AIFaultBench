#!/usr/bin/env python3
"""Offline reproduction for SWE-agent issue #1078 at the pinned buggy revision."""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace


LIMIT = 65_536
ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "codebase" / "sweagent" / "run" / "hooks" / "open_pr.py"


def install_module(name: str, **attributes: object) -> ModuleType:
    module = ModuleType(name)
    module.__dict__.update(attributes)
    sys.modules[name] = module
    return module


class FakeHTTP422(RuntimeError):
    """What GitHub returns when a pull request body exceeds its documented limit."""


class FakePulls:
    def create(self, **kwargs: object) -> SimpleNamespace:
        body = kwargs["body"]
        assert isinstance(body, str)
        if len(body) > LIMIT:
            raise FakeHTTP422(
                f"HTTP 422: body is too long (maximum is {LIMIT} characters); got {len(body)}"
            )
        return SimpleNamespace(html_url="https://example.invalid/pull/1")


class FakeGhApi:
    def __init__(self, token: str) -> None:
        self.pulls = FakePulls()


class FakeEnv:
    def communicate(self, **_kwargs: object) -> str:
        return ""


class FakeLogger:
    def info(self, *_args: object, **_kwargs: object) -> None:
        pass

    def debug(self, *_args: object, **_kwargs: object) -> None:
        pass


def load_buggy_hook() -> ModuleType:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"Pinned checkout is missing: {SOURCE}")

    # The hook imports these collaborators at module load.  They are all replaced by
    # local doubles so the real GitHub API is never contacted.
    install_module("ghapi")
    install_module("ghapi.all", GhApi=FakeGhApi)
    install_module("pydantic", BaseModel=object)
    install_module("sweagent")
    install_module("sweagent.environment")
    install_module("sweagent.environment.swe_env", SWEEnv=object)
    install_module("sweagent.run")
    install_module("sweagent.run.hooks")
    install_module("sweagent.run.hooks.abstract", RunHook=object)
    install_module("sweagent.types", AgentRunResult=object)
    install_module(
        "sweagent.utils.github",
        InvalidGithubURL=ValueError,
        _get_gh_issue_data=lambda _url, token: SimpleNamespace(number=123, title="large trajectory"),
        _get_associated_commit_urls=lambda *_args, **_kwargs: [],
        _parse_gh_issue_url=lambda _url: ("example", "repo", 123),
    )
    install_module("sweagent.utils")
    install_module("sweagent.utils.log", get_logger=lambda *_args, **_kwargs: FakeLogger())

    spec = importlib.util.spec_from_file_location("buggy_open_pr", SOURCE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.random.random = lambda: 0.12345678
    return module


def main() -> None:
    hook = load_buggy_hook()
    # One oversized observation is enough: format_trajectory_markdown copies it into
    # the PR description verbatim in the buggy revision.
    trajectory = [{"response": "", "observation": "x" * LIMIT}]
    try:
        hook.open_pr(
            logger=FakeLogger(),
            token="offline-token",
            env=FakeEnv(),
            github_url="https://github.com/example/repo/issues/123",
            trajectory=trajectory,
        )
    except FakeHTTP422 as error:
        print(f"BUG REPRODUCED: {error}")
        raise SystemExit(1)

    raise AssertionError("BUG NOT PRESENT: PR body was truncated before the simulated GitHub call")


if __name__ == "__main__":
    main()

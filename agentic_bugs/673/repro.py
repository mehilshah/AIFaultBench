#!/usr/bin/env python3
"""Offline reproduction for agno Team SSE accumulator leakage (issue #8235)."""

import asyncio
import sys

from agno.os.routers.teams.router import team_response_streamer
from agno.run.team import TeamRunOutput


class OfflineTeam:
    """A model-free team double that leaks an accumulator into its async stream."""

    def arun(self, **kwargs):
        assert kwargs["stream"] is True
        assert kwargs["stream_events"] is True
        return self._stream()

    async def _stream(self):
        yield TeamRunOutput(run_id="accumulator-only", content="final result")


async def main() -> int:
    accumulator = TeamRunOutput(run_id="accumulator-only")
    assert not hasattr(accumulator, "event")
    assert hasattr(accumulator, "events")

    frames = [
        frame
        async for frame in team_response_streamer(OfflineTeam(), "offline reproduction")
    ]
    expected_error = "'TeamRunOutput' object has no attribute 'event'"
    if len(frames) == 1 and "event: TeamRunError" in frames[0] and expected_error in frames[0]:
        # The router catches the formatter crash and converts it to this SSE error frame.
        assert expected_error in frames[0]
        print("OBSERVED: TeamRunOutput reached the SSE formatter and triggered AttributeError")
        return 1

    print("NOT_REPRODUCED: TeamRunOutput was filtered before SSE formatting")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

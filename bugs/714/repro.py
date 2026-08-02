#!/usr/bin/env python3
"""Offline reproduction for frozen vertices without Langflow's cache service."""

import asyncio
from collections import deque
from unittest.mock import patch

from lfx.graph.graph.base import Graph


class RunManager:
    def add_to_vertices_being_run(self, vertex_id):
        del vertex_id


class FrozenVertex:
    id = "frozen-vertex"
    frozen = True
    display_name = "Test Component"
    is_loop = False


class MinimalGraph:
    """Only the Graph state touched before the faulty cache access."""

    _prepared = True
    _run_queue = deque(["frozen-vertex"])
    run_manager = RunManager()
    get_next_in_queue = Graph.get_next_in_queue
    build_vertex = Graph.build_vertex

    def get_vertex(self, vertex_id):
        assert vertex_id == "frozen-vertex"
        return FrozenVertex()


async def reproduce():
    # This forces Graph.astep to choose its offline fallback cache function.
    with patch("lfx.graph.graph.base.get_chat_service", return_value=None):
        await Graph.astep(MinimalGraph())


try:
    asyncio.run(reproduce())
except TypeError as error:
    expected = "'NoneType' object is not subscriptable"
    assert str(error) == expected, f"unexpected TypeError: {error!s}"
    print(f"BUG REPRODUCED: TypeError: {error}")
    raise
else:
    raise AssertionError("expected a frozen vertex without cache service to raise TypeError")

#!/usr/bin/env python3
"""Offline reproduction for CrewAI issue #5474."""

from crewai.mcp import tool_resolver
from crewai.mcp.config import MCPServerStdio


class Logger:
    def log(self, *_args: object) -> None:
        pass


class FakeMCPClient:
    """A local MCP discovery double; it never starts a process or uses a socket."""

    def __init__(self, **_kwargs: object) -> None:
        self.connected = False

    async def connect(self) -> None:
        self.connected = True

    async def disconnect(self) -> None:
        self.connected = False

    async def list_tools(self) -> list[dict[str, object]]:
        simple_schema = {
            "type": "object",
            "properties": {"query": {"type": "string"}},
        }
        recursive_schema = {
            "type": "object",
            "properties": {"node": {"$ref": "#/$defs/Node"}},
            "$defs": {
                "Node": {
                    "type": "object",
                    "properties": {"child": {"$ref": "#/$defs/Node"}},
                }
            },
        }
        return [
            {"name": f"tool_{number}", "inputSchema": simple_schema}
            for number in range(10)
        ] + [{"name": "recursive_tool", "inputSchema": recursive_schema}]


tool_resolver.MCPClient = FakeMCPClient
resolver = tool_resolver.MCPToolResolver(agent=None, logger=Logger())

try:
    resolver._resolve_native(MCPServerStdio(command="offline-fake", args=[]))
except RuntimeError as error:
    expected = "Failed to get native MCP tools: maximum recursion depth exceeded"
    assert str(error) == expected, repr(error)
    print(f"OBSERVED BUG: {error}")
    raise
else:
    raise AssertionError("Expected recursive MCP schema to make native tool resolution fail")

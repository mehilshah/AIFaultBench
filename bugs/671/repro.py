#!/usr/bin/env python3
"""Offline reproduction for pydantic-ai issue #6331."""

from pydantic_ai import Agent
from pydantic_ai.capabilities import NativeTool
from pydantic_ai.exceptions import UserError
from pydantic_ai.models.test import TestModel
from pydantic_ai.native_tools import CodeExecutionTool, MCPServerTool


def dynamic_capability(_ctx: object) -> NativeTool:
    """Materialize a native tool only when the capability is resolved for a run."""
    return NativeTool(MCPServerTool(id='dyn', url='https://mcp.example.com/dyn'))


model = TestModel()
agent = Agent(model=model)

try:
    with agent.override(native_tools=[CodeExecutionTool()]):
        agent.run_sync('Hello', capabilities=[dynamic_capability])
except UserError as exc:
    assert str(exc) == 'TestModel does not support built-in tools', repr(exc)
else:
    raise AssertionError('TestModel should reject the native-tool request after recording it')

request = model.last_model_request_parameters
assert request is not None, 'TestModel did not record model request parameters'
native_tools = request.native_tools
assert any(isinstance(tool, CodeExecutionTool) for tool in native_tools), native_tools

if not any(isinstance(tool, MCPServerTool) and tool.id == 'dyn' for tool in native_tools):
    print('OBSERVED BUG: override request dropped dynamic MCPServerTool(id="dyn").')
    raise AssertionError(f'expected dynamic MCP tool alongside override; got {native_tools!r}')

print('BUG NOT OBSERVED: dynamic MCPServerTool(id="dyn") reached the overridden request.')

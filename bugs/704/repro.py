#!/usr/bin/env python3
"""Offline reproduction for pydantic-ai issue #6051."""

from pydantic_ai.models import ModelRequestParameters
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.native_tools import CodeExecutionTool
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.tools import ToolDefinition


def main() -> None:
    # Constructing the provider with a dummy key does not make a request. This script only
    # calls the local request-configuration builder and never invokes a model client.
    model = GoogleModel(
        'gemini-3.1-pro-preview',
        provider=GoogleProvider(api_key='offline-dummy-key'),
        profile={'google_supports_server_side_tool_invocations': True},
    )
    parameters = ModelRequestParameters(
        function_tools=[ToolDefinition(name='add', parameters_json_schema={'type': 'object'})],
        native_tools=[CodeExecutionTool()],
    )

    _tools, tool_config, _image_config = model._get_tool_config(parameters, {})
    flag = (tool_config or {}).get('include_server_side_tool_invocations')

    if flag is True:
        print('NOT REPRODUCED: CodeExecutionTool correctly enables include_server_side_tool_invocations')
        return

    print(
        'BUG REPRODUCED: CodeExecutionTool plus a function tool produced '
        f'include_server_side_tool_invocations={flag!r}'
    )
    raise AssertionError(
        'GoogleModel omitted include_server_side_tool_invocations for CodeExecutionTool with function calling'
    )


if __name__ == '__main__':
    main()

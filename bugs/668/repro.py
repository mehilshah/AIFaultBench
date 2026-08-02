#!/usr/bin/env python3
"""Offline reproduction for pydantic-ai issue #6771."""

from google.genai import models

from pydantic_ai.models import ModelRequestParameters
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.native_tools import WebFetchTool
from pydantic_ai.profiles.google import google_model_profile
from pydantic_ai.providers import Provider
from pydantic_ai.tools import ToolDefinition


class OfflineVertexProvider(Provider[object]):
    """Supplies the Google model profile without constructing a network client."""

    @property
    def name(self) -> str:
        return 'google-cloud'

    @property
    def base_url(self) -> str:
        return 'https://offline.invalid'

    @property
    def client(self) -> object:
        return object()

    model_profile = staticmethod(google_model_profile)


def main() -> None:
    model = GoogleModel('gemini-3.5-flash-lite', provider=OfflineVertexProvider())
    parameters = ModelRequestParameters(
        function_tools=[ToolDefinition(name='find_things')],
        native_tools=[WebFetchTool()],
    )
    _, tool_config, _ = model._get_tool_config(parameters, {})

    assert tool_config is not None
    assert tool_config.get('include_server_side_tool_invocations') is True

    try:
        models._ToolConfig_to_vertex(tool_config)
    except ValueError as exc:
        expected = 'include_server_side_tool_invocations parameter is not supported in Gemini Enterprise Agent Platform.'
        assert str(exc) == expected
        print(f'OBSERVED BUG: {type(exc).__name__}: {exc}', flush=True)
        raise SystemExit(1)
    else:
        raise AssertionError('Vertex converter unexpectedly accepted include_server_side_tool_invocations')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Offline reproduction for CodeAgent's premature executor-type validation."""

import sys

from smolagents import CodeAgent


class CustomCodeAgent(CodeAgent):
    factory_called = False

    def create_python_executor(self):
        type(self).factory_called = True
        return object()


try:
    CustomCodeAgent(tools=[], model=object(), executor_type="my_executor")
except ValueError as error:
    assert str(error) == "Unsupported executor type: my_executor", repr(error)
    assert not CustomCodeAgent.factory_called, "the custom executor factory unexpectedly ran"
    print("OBSERVED BUG: unsupported custom executor rejected before overridden factory ran")
    sys.exit(1)
else:
    assert CustomCodeAgent.factory_called, "custom executor factory was not called"
    print("BUG NOT OBSERVED: overridden factory accepted the custom executor type")

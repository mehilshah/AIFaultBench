#!/usr/bin/env python3
"""Reproduce pydantic-ai#6215 without a Temporal service or an LLM provider."""

from datetime import datetime, timezone

from pydantic_ai.durable_exec.temporal import _workflow_runner
from pydantic_ai.messages import ModelResponse, TextPart
from pydantic_ai.usage import RequestUsage
from temporalio import workflow
from temporalio.worker.workflow_sandbox import SandboxedWorkflowRunner
from temporalio.worker.workflow_sandbox._importer import Importer
from temporalio.worker.workflow_sandbox._restrictions import (
    RestrictedWorkflowAccessError,
    RestrictionContext,
)


EXPECTED_MESSAGE = 'Cannot access urllib.request.Request.__mro_entries__ from inside a workflow.'


def main() -> None:
    # This is the same runner transformation supplied by PydanticAIPlugin to a Temporal worker.
    runner = _workflow_runner(SandboxedWorkflowRunner())
    assert 'genai_prices' not in runner.restrictions.passthrough_modules
    assert 'httpx2' not in runner.restrictions.passthrough_modules

    response = ModelResponse(
        parts=[TextPart('ok')],
        usage=RequestUsage(input_tokens=100, output_tokens=10),
        model_name='claude-sonnet-4-5',
        provider_name='anthropic',
        timestamp=datetime(2026, 7, 2, tzinfo=timezone.utc),
    )
    importer = Importer(runner.restrictions, RestrictionContext())
    importer.restriction_context.is_runtime = True

    try:
        workflow.unsafe._set_in_sandbox(True)
        # `cost()` lazily imports genai_prices.data. The sandbox reimports its httpx2
        # dependency, where subclass creation accesses the restricted Request proxy.
        with importer.applied():
            response.cost()
    except RestrictedWorkflowAccessError as exc:
        if EXPECTED_MESSAGE not in str(exc):
            raise AssertionError(f'Unexpected sandbox error: {exc}') from exc
        print(f'OBSERVED BUG: {type(exc).__name__}: {EXPECTED_MESSAGE}')
        raise RuntimeError('BUG REPRODUCED: pricing lazy import is blocked by the Temporal sandbox') from exc
    else:
        raise AssertionError('Bug did not reproduce: response.cost() completed inside the Temporal sandbox')
    finally:
        workflow.unsafe._set_in_sandbox(False)
        importer.restriction_context.is_runtime = False


if __name__ == '__main__':
    main()

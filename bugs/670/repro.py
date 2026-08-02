#!/usr/bin/env python3
"""Reproduce pydantic-ai #6415 without NumPy or any model/provider call."""

from pydantic_ai.messages import ModelRequest, ToolReturnPart


class AmbiguousComparison:
    def __bool__(self) -> bool:
        raise ValueError('The truth value of an array with more than one element is ambiguous')


class ArrayLike:
    """Minimal stand-in for NumPy's non-scalar ``array != value`` result."""

    def __ne__(self, other: object) -> AmbiguousComparison:
        return AmbiguousComparison()

    def __repr__(self) -> str:
        return 'ArrayLike([1, 2, 3])'


part = ToolReturnPart(tool_name='get_array', content=ArrayLike(), tool_call_id='fixed-tool-call-id')
message = ModelRequest(parts=[part])

try:
    repr(part)
except ValueError as exc:
    expected = 'The truth value of an array with more than one element is ambiguous'
    assert str(exc) == expected, repr(exc)
    try:
        repr(message)
    except ValueError as nested_exc:
        assert str(nested_exc) == expected, repr(nested_exc)
    else:
        raise AssertionError('ModelRequest repr unexpectedly succeeded')
    print(f'OBSERVED BUG: ToolReturnPart and ModelRequest repr raise ValueError: {exc}', flush=True)
    raise
else:
    raise AssertionError('Expected repr() to raise ValueError for a non-boolean __ne__ result')

#!/usr/bin/env python3
"""Offline reproduction for langchain-ai/langchain issue #37912."""

from langchain_core.messages import AIMessage, ToolMessage
from langchain_perplexity import ChatPerplexity


def main() -> None:
    # Construction and conversion are local operations; no provider client is invoked.
    llm = ChatPerplexity(model="sonar", api_key="dummy")
    tool_call = {
        "id": "call_1",
        "name": "search",
        "args": {"q": "x"},
        "type": "tool_call",
    }
    assistant_payload = llm._convert_message_to_dict(
        AIMessage(content="", tool_calls=[tool_call])
    )

    try:
        llm._convert_message_to_dict(
            ToolMessage(content="result", tool_call_id="call_1")
        )
    except TypeError as exc:
        tool_error = str(exc)
    else:
        tool_error = None

    expected_error = "Got unknown type content='result' tool_call_id='call_1'"
    if "tool_calls" not in assistant_payload and tool_error == expected_error:
        print(
            "BUG REPRODUCED: AIMessage tool_calls were dropped; "
            f"ToolMessage raised TypeError: {tool_error}"
        )
        raise SystemExit(1)

    if "tool_calls" in assistant_payload and tool_error is None:
        print("BUG NOT REPRODUCED: both message types serialized successfully")
        return

    raise AssertionError(
        "Unexpected converter behavior: "
        f"assistant_payload={assistant_payload!r}, tool_error={tool_error!r}"
    )


if __name__ == "__main__":
    main()

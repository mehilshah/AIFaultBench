#!/usr/bin/env python3
"""Offline reproduction for langgraph issue #6578."""

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.types import Command

tool_returned = False


@tool(description="Ask a clarification question.")
def clarify_user(question: str, runtime: ToolRuntime) -> Command:
    global tool_returned
    tool_returned = True
    return Command(
        goto="__end__",
        update={
            "messages": [
                ToolMessage(
                    content="success",
                    tool_call_id=runtime.tool_call_id,
                    name="clarify_user",
                ),
                AIMessage(content=question),
            ]
        },
    )


class CountingFakeChatModel(FakeMessagesListChatModel):
    calls: int = 0

    def bind_tools(self, tools, **kwargs):
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        self.calls += 1
        if self.calls > 1:
            raise RuntimeError(
                "BUG: model invoked after Command(goto='__end__') returned from tool"
            )
        return super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)


model = CountingFakeChatModel(
    responses=[
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "clarify_user",
                    "args": {"question": "What do you mean?"},
                    "id": "call_1",
                }
            ],
        )
    ]
)
agent = create_agent(model=model, tools=[clarify_user])

try:
    agent.invoke({"messages": [HumanMessage(content="hello")]})
except RuntimeError as exc:
    if tool_returned and str(exc).startswith("BUG: model invoked after"):
        print("OBSERVED: Command(goto='__end__') did not stop the agent loop")
        raise SystemExit(1)
    raise
else:
    raise AssertionError("Command(goto='__end__') stopped the agent loop; bug absent")

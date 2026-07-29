#!/usr/bin/env python3
"""Offline reproduction for agno Workflow async-session loading bug."""

import asyncio
import warnings

from agno.db.base import AsyncBaseDb
from agno.session.workflow import WorkflowSession
from agno.workflow.workflow import Workflow


async def get_session(self, session_id, session_type=None, user_id=None, deserialize=True):
    return self.session


def unused_abstract_method(*args, **kwargs):
    return None


# AsyncBaseDb has many unrelated abstract persistence methods.  Supplying inert
# implementations keeps this fake focused solely on the async get_session API.
fake_methods = {name: unused_abstract_method for name in AsyncBaseDb.__abstractmethods__}
fake_methods["get_session"] = get_session
FakeAsyncDb = type("FakeAsyncDb", (AsyncBaseDb,), fake_methods)

expected = WorkflowSession(session_id="stored-session")
db = FakeAsyncDb()
db.session = expected
workflow = Workflow(db=db, session_id=expected.session_id, telemetry=False)

# The asynchronous helper proves the fake backend has a valid stored session.
assert asyncio.run(workflow.aget_session()) is expected

# At the buggy commit this invokes the async method without await, then rejects
# its coroutine object because it is not a WorkflowSession.
warnings.simplefilter("always", RuntimeWarning)
actual = workflow.get_session()
if actual is None:
    print("BUG REPRODUCED: Workflow.get_session returned None for an async stored session")
    raise AssertionError("async db.get_session was called without await")

print("BUG NOT REPRODUCED: Workflow.get_session loaded the async stored session")

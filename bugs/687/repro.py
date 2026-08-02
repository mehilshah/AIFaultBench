#!/usr/bin/env python3
"""Check whether MultiQueryRetriever deduplicates list metadata without hashing it."""

from langchain_core.documents import Document
from langchain_classic.retrievers.multi_query import MultiQueryRetriever


documents = [
    Document(
        page_content="Python is great",
        metadata={"tags": ["python", "programming"], "source": "web"},
    ),
    Document(
        page_content="Python is great",
        metadata={"tags": ["python", "programming"], "source": "web"},
    ),
]

# ``unique_union`` needs no instance state.  Calling the real method directly keeps
# the test offline and isolates the reported hash-key operation.
unique = MultiQueryRetriever.unique_union(None, documents)
assert unique == [documents[0]], f"unexpected deduplication result: {unique!r}"
print("NOT_REPRODUCED: list metadata was deduplicated without TypeError (1 document)")

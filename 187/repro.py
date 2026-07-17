from __future__ import annotations

import asyncio
import traceback
import sys

import numpy as np

from marimo._ast.app import App
from tests.conftest import MockedKernel


app = App()


@app.cell
def __():
    import marimo as mo

    return (mo,)


@app.cell
def __(arr, mo):
    mo.md(f"`{arr.shape = }`")


async def main() -> None:
    kernel = MockedKernel()
    try:
        first = await app.embed(defs={"arr": np.ones(1)})
        print("first output:", first.output.text)

        second = await app.embed(defs={"arr": np.zeros(2)})
        print("second output:", second.output.text)
    finally:
        kernel.teardown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        traceback.print_exc()
        sys.exit(1)

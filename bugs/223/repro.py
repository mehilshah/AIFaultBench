#!/usr/bin/env python3
"""Minimal repro for Triton grid canonicalization failing on int grid results."""

from collections import OrderedDict
from types import SimpleNamespace
import traceback

import triton
import triton.language as tl
import triton.runtime.jit as jitmod


class FakeDriver:
    def get_current_device(self):
        return 0

    def get_current_stream(self, device):
        return None


class DummyKernel:
    packed_metadata = object()
    function = object()

    def launch_metadata(self, grid, stream, *args):
        print(f"launch_metadata(grid={grid!r}, stream={stream!r})")

    def run(self, *args, **kwargs):
        print("Dummy kernel run reached unexpectedly")


def install_fakes():
    # Keep the repro on Triton's real JITFunction.run() path while avoiding CUDA.
    jitmod.driver._active = FakeDriver()
    jitmod.driver._default = FakeDriver()

    def fake_create_binder(self):
        def binder(*args, **kwargs):
            bound_args = OrderedDict(
                [
                    ("x_ptr", args[0]),
                    ("n_element", args[1]),
                    ("BLOCK_SIZE", kwargs["BLOCK_SIZE"]),
                ]
            )
            specialization = [
                ("pointer", None),
                ("i32", None),
                ("constexpr", kwargs["BLOCK_SIZE"]),
            ]
            options = SimpleNamespace()
            return bound_args, specialization, options

        return {}, {}, None, None, binder

    def fake_pack_args(self, backend, kwargs, bound_args, specialization, options):
        packed_options = SimpleNamespace(
            num_warps=1,
            num_ctas=1,
            num_stages=1,
            enable_fp_fusion=False,
            launch_cooperative_grid=False,
            extern_libs={},
        )
        signature = {"x_ptr": "pointer", "n_element": "i32", "BLOCK_SIZE": "constexpr"}
        constexprs = {"BLOCK_SIZE": bound_args["BLOCK_SIZE"]}
        attrs = {}
        return packed_options, signature, constexprs, attrs

    def fake_do_compile(self, *args, **kwargs):
        print("fake compile reached")
        return DummyKernel()

    jitmod.JITFunction.create_binder = fake_create_binder
    jitmod.JITFunction._pack_args = fake_pack_args
    jitmod.JITFunction._do_compile = fake_do_compile


install_fakes()


@triton.jit
def add_kernel(x_ptr, n_element, BLOCK_SIZE: tl.constexpr):
    pass


def main():
    n_element = 98432
    grid = lambda meta: triton.cdiv(n_element, meta["BLOCK_SIZE"])

    print(f"triton_version={triton.__version__}")
    print("launching kernel with grid callable that returns int")

    add_kernel[grid](123, n_element, BLOCK_SIZE=1024)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        raise

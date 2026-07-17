# POT issue 117 repro

This folder reproduces the crash reported in:
`https://github.com/PythonOT/POT/issues/117`

The failure occurs when calling `ot.emd([], [], M)` with a very large
`50000 x 50000` cost matrix. On this codebase (`POT 0.6.0`), the C++
transport solver aborts with:

```text
terminate called after throwing an instance of 'std::length_error'
  what():  vector::_M_default_append
```

## Why it happens

The implementation in `codebase/ot/lp/EMD_wrapper.cpp` constructs the
network simplex with `n * m` edge capacity. For a `50000 x 50000` matrix,
`n * m` overflows a 32-bit `int` and the solver fails before it can finish.

## Reproduction

1. Create the local virtual environment and install the dependencies:
   `./setup_env.sh`
2. Run the repro:
   `./run_repro.sh`

The default matrix size is `50000`, but it can be overridden with `N=...`
when invoking `repro.py`.

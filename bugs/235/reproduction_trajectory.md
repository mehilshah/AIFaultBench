# Reproduction Trajectory — Bug 235: equinox

- **Bug report:** [https://github.com/patrick-kidger/equinox/issues/791](https://github.com/patrick-kidger/equinox/issues/791)
- **Repository:** patrick-kidger/equinox @ `028a6f4`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local Python 3.12 virtual environment and install the pinned runtime from requirements.txt.
2. Install the local codebase in editable mode so equinox metadata is available.
3. Run ./setup_env.sh and then ./run_repro.sh to observe the __getattr__ hits during Foo().moo().

## Observed behavior

- Running ./run_repro.sh prints __getattr__ hits for __name__ and __qualname__ when calling Foo().moo().
- The repro exits with status 1 after confirming the method call returned moo and triggered the two getattr lookups.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./setup_env.sh && ./run_repro.sh
```

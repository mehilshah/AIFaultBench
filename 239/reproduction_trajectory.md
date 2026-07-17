# Reproduction Trajectory — Bug 239: cibuildwheel

- **Bug report:** [https://github.com/pypa/cibuildwheel/issues/1724](https://github.com/pypa/cibuildwheel/issues/1724)
- **Repository:** pypa/cibuildwheel @ `93542c3`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Generated a minimal C++ extension project matching the issue report's setup pattern.
2. Built and installed the project locally with pip, then called the exported create_context() function.
3. Built a cp310 manylinux wheel with the local cibuildwheel source tree and imported the result in the manylinux container.

## Observed behavior

- Local host build output includes 32 for sizeof(std::string).
- The cp310 wheel built by cibuildwheel crashes when imported in the manylinux container.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

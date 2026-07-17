# Bug 239 Repro Bundle

This folder contains a self-contained reproduction attempt for
`https://github.com/pypa/cibuildwheel/issues/1724`.

What the bundle does:
- builds a small scikit-build/pybind11 project that prints `sizeof(std::string)`
- verifies the local host build
- attempts the Linux cibuildwheel path against the report's manylinux image

Current outcome in this environment:
- the local host build succeeds and prints `sizeof(std::string) = 32`
- the cibuildwheel manylinux image cannot be pulled here because Docker fails while extracting a layer
- the bug is therefore not reproducible end to end in this folder as-is

Files:
- [`repro.py`](./repro.py)
- [`requirements.txt`](./requirements.txt)
- [`setup_env.sh`](./setup_env.sh)
- [`run_repro.sh`](./run_repro.sh)
- [`reproduction.json`](./reproduction.json)
- [`repro_stdout.log`](./repro_stdout.log)
- [`repro_stderr.log`](./repro_stderr.log)

Run:
```bash
bash run_repro.sh
```

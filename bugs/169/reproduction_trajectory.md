# Reproduction Trajectory — Bug 169: kornia

- **Bug report:** [https://github.com/kornia/kornia/issues/3371](https://github.com/kornia/kornia/issues/3371)
- **Repository:** kornia/kornia @ `30eec36`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Open codebase/README.md and codebase/README_zh-CN.md.
2. Inspect the license badge link targets at the badge lines.
3. Verify that codebase/LICENSE exists and codebase/LICENCE does not exist.
4. Run ./run_repro.sh to confirm the missing target is detected.

## Observed behavior

- codebase/README.md and codebase/README_zh-CN.md both link the license badge to LICENCE (see lines 23 and 25).
- The repository root contains LICENSE but no LICENCE file.
- Running ./run_repro.sh exits with status 1 and prints BUG REPRODUCED.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

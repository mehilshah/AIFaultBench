# Reproduction Trajectory — Bug 279: sdv

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2915](https://github.com/sdv-dev/SDV/issues/2915)
- **Repository:** sdv-dev/SDV @ `1b836b1d6edc142b389de94913fdf2c3d3acfa54`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Read `bug_report.txt` and identified the reported failure as a `ColumnFormula` serialization crash in SDV Enterprise 0.47.4.
2. Inspected the local `codebase/` for `ColumnFormula` and sandbox support.
3. Confirmed that the checked-in source tree exports only the open-source CAG classes and does not define `ColumnFormula`.

## Observed behavior

- See the captured logs below for the observed output.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The local repository is open-source SDV 1.37.3.dev1 and does not contain the enterprise `ColumnFormula` constraint or an `sdv.cag.sandbox` module, so the reported crash cannot be exercised from this source tree.

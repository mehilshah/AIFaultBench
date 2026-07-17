# Reproduction Trajectory — Bug 136: deepvariant

- **Bug report:** [https://github.com/google/deepvariant/issues/897](https://github.com/google/deepvariant/issues/897)
- **Repository:** google/deepvariant @ `64da16d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Open `codebase/docs/deepvariant-details.md`.
2. Read the first line and compare it to the expected heading.
3. Run `bash run_repro.sh` to confirm the typo is present.

## Observed behavior

- codebase/docs/deepvariant-details.md line 1 is `f# DeepVariant usage guide` instead of `# DeepVariant usage guide`.
- Running `bash run_repro.sh` produced `{"file": "codebase/docs/deepvariant-details.md", "expected_first_line": "# DeepVariant usage guide", "observed_first_line": "f# DeepVariant usage guide", "reproduced": true}`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

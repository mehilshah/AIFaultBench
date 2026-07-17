# Reproduction Trajectory — Bug 373: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2839](https://github.com/sdv-dev/SDV/issues/2839)
- **Repository:** sdv-dev/SDV @ `1244df91a41dae7100975d6e4db8253a72b29b66`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a minimal virtualenv with the metadata-layer dependencies.
2. Loaded the local `codebase/` source tree through the repro script.
3. Called `Metadata.load_from_dict(...)` with `parent_primary_key='other'` and ran `metadata.visualize()`.
4. Observed that the rendered edge label used the table primary key (`fk → pk`) instead of the relationship key (`fk → other`).

## Observed behavior

- Running the repro produced graph source with `parent -> child [label="  fk → pk" arrowhead=oinv]`. The script printed `contains_fk_to_other: False` and failed with `AssertionError: Expected relationship label 'fk → other' but got ...`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && ./run_repro.sh
```

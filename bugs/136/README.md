# Bug 136 Reproduction

This bundle reproduces the typo reported in DeepVariant issue 897.

Observed behavior:
- `codebase/docs/deepvariant-details.md` starts with `f# DeepVariant usage guide`

Expected behavior:
- The first line should be `# DeepVariant usage guide`

Run:
```bash
bash run_repro.sh
```

The script reports the observed first line and exits successfully when the typo
is present.

# MMS Forced Alignment Shape Mismatch Reproduction

This bundle reproduces the forced-alignment failure reported in fairseq issue
5123.

The original bug is in `examples/mms/data_prep/align_and_segment.py`, where
sliding-window emission tensors are concatenated with `torch.cat(..., dim=1)`.
When the windows produce different time lengths, concatenation fails with a
shape mismatch.

## Run

```bash
bash run_repro.sh
```

The run writes:

- `repro_stdout.log`
- `repro_stderr.log`

The repro exits with the concatenation error.

## Why this is minimal

The upstream script depends on a downloaded MMS alignment model, `torchaudio`,
and `sox`. This reproduction keeps only the windowing and concatenation logic
that triggers the failure, so it is deterministic and does not require the
original assets.

# Reproduction Trajectory — Bug 623: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21429](https://github.com/Lightning-AI/pytorch-lightning/issues/21429)
- **Repository:** Lightning-AI/pytorch-lightning @ `5130530c6eda2fbe971e1d3cef83dc474af11c6e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a synthetic MiniLibriMix-style metadata directory with length stored as 48000.0 so pandas reads it back as numpy.float64.
2. Loaded asteroid.data.librimix_dataset.LibriMix directly from the installed Asteroid source tree without importing the full package stack.
3. Monkeypatched LibriMix.mini_from_download to point loaders_from_mini at the synthetic fixture.
4. Iterated the first batch from the returned DataLoader and reproduced the TypeError.

## Observed behavior

- The repro prints length_type=float64 and then fails when iterating the first batch. The traceback ends in asteroid/data/librimix_dataset.py:92 at random.randint(0, row["length"] - self.seg_len), which passes a numpy.float64 into random.randrange and raises TypeError: 'numpy.float64' object cannot be interpreted as an integer.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

# Reproduction Trajectory — Bug 044: fairseq

- **Bug report:** [https://github.com/facebookresearch/fairseq/issues/5142](https://github.com/facebookresearch/fairseq/issues/5142)
- **Repository:** facebookresearch/fairseq @ `1082b61b12ec92d6c813906fcec90139b85fb039`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Inspect examples/mms/tts/infer.py and note the filter_oov() print.
2. Use the official MMS Japanese vocab extracted from jvn.tar.gz.
3. Run the same OOV filtering on Japanese-script input.

## Observed behavior

- The MMS Japanese vocab in jvn.tar.gz does not contain Japanese characters.
- filter_oov() prints an empty string for Japanese-script input.
- The filtered text length is 0, so downstream inference would receive empty text.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

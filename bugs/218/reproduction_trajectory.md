# Reproduction Trajectory — Bug 218: stanza

- **Bug report:** [https://github.com/stanfordnlp/stanza/issues/1366](https://github.com/stanfordnlp/stanza/issues/1366)
- **Repository:** stanfordnlp/stanza
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a sentence containing a multi-word token and loaded the local Stanza data-object modules without the broken global torch.
2. Called sentence.to_dict() and iterated over the returned dictionaries the same way described in the bug report.
3. Observed that the multi-word-token dictionary has no xpos key and that indexing entry["xpos"] raises KeyError: 'xpos'.

## Observed behavior

- Running ./run_repro.sh prints a sentence.to_dict() entry with id (5, 6) that lacks xpos, then crashes on entry["xpos"] with KeyError: 'xpos'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

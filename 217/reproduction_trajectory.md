# Reproduction Trajectory — Bug 217: stanza

- **Bug report:** [https://github.com/stanfordnlp/stanza/issues/1357](https://github.com/stanfordnlp/stanza/issues/1357)
- **Repository:** stanfordnlp/stanza @ `17eb6fc`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create and activate the isolated Python 3.11 environment with setup_env.sh.
2. Run repro.py with STANZA_RESOURCES_DIR pointing at the local stanza_resources/ directory.
3. Observe the POS trainer initialization crash with KeyError: 'bert_finetune'.

## Observed behavior

- Pipeline('en', package='mimic', processors={'ner': 'i2b2'}) fails in codebase/stanza/models/pos/trainer.py with KeyError: 'bert_finetune'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

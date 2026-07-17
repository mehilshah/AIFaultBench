# Reproduction Trajectory — Bug 261: stanza

- **Bug report:** [https://github.com/stanfordnlp/stanza/issues/1423](https://github.com/stanfordnlp/stanza/issues/1423)
- **Repository:** stanfordnlp/stanza @ `d29896f`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated venv and installed the local codebase plus its runtime dependencies.
2. Downloaded the Portuguese tokenizer resources into a local stanza_resources directory.
3. Ran a Pipeline(lang='pt', processors='tokenize') on the reported URL example and observed sentence splitting at each dot.
4. Ran the reported 'www.' control example and observed the expected single sentence.

## Observed behavior

- Using the local stanza 1.9.2 codebase, the Portuguese tokenizer splits 'exemplo1.com, exemplo2.com e exemplo3.com.br' into multiple sentences. The control case with 'www.' stays as one sentence.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

# Reproduction Trajectory — Bug 133: flair

- **Bug report:** [https://github.com/flairNLP/flair/issues/3665](https://github.com/flairNLP/flair/issues/3665)
- **Repository:** flairNLP/flair @ `ee8596c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Sentence from `I am a student named John\nSmith.` using the local Flair source files.
2. Build the span covering `John` and `Smith`, attach an `ner` label, and retrieve it through `sentence.get_spans('ner')`.
3. Compare `entity.text` with the original source slice at `entity.start_position:entity.end_position`; the newline is rendered as a space, so the assertion fails.

## Observed behavior

- The packaged repro prints `Sentence[8]: "I am a student named John\nSmith." -> ["John Smith"/PER]` and then fails `assert example[entity.start_position:entity.end_position] == entity.text` because the source slice is `John\nSmith` while `entity.text` is `John Smith`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
REPRO_PYTHON=/tmp/bug133cpu/bin/python bash ./run_repro.sh
```

# Bug Reproduction

This folder reproduces the Flair span-text mismatch reported in `bug_report.txt`.

## What happens

The local Flair `Span.text` implementation rebuilds span text from token texts plus spaces, so a newline inside an entity becomes a space in the extracted span text.

## Run

```bash
./run_repro.sh
```

`run_repro.sh` will create a local virtual environment if needed, install the minimal dependencies from `requirements.txt`, and execute `repro.py`.

## Expected result

The script prints a span whose text is `John Smith` while the original source slice is `John\nSmith`, then fails the assertion.

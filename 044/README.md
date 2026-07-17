# Bug 044

Repro bundle for fairseq MMS TTS issue #5142.

Reproduction status: reproducible.

## What fails

`examples/mms/tts/infer.py` filters input text through the model vocab before synthesis:

- the Japanese MMS package (`jvn.tar.gz`) ships a vocab that contains Latin letters, digits, and punctuation
- Japanese-script input is filtered down to an empty string
- the script prints `text after filtering OOV:` with nothing after the colon

## Files

- `repro.py`: self-contained repro of the OOV filtering behavior
- `fixtures/jvn/vocab.txt`: vocab extracted from the official Japanese MMS bundle
- `run_repro.sh`: runs the repro and captures logs
- `setup_env.sh`: creates a local virtualenv if needed
- `requirements.txt`: no extra dependencies required
- `reproduction.json`: machine-readable result written by the repro

## Run

```bash
bash run_repro.sh
```

Expected outcome:

- `text after filtering OOV:` is followed by an empty value
- `reproduction.json` reports `reproducible: true`

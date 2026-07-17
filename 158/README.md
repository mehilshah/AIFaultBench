# Bug 158

This folder is the reusable standardized benchmark input for this bug.

The reported defect is in `Phi4MultimodalConfig.__init__`:

- `vision_config` stays `None` when the config is built with no arguments.
- `audio_config` also stays `None` when a non-`None` `vision_config` is supplied.

Run the repro bundle with:

```bash
bash run_repro.sh
```

Reproduction artifacts:

- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Source summary:

- issue URL: `https://github.com/huggingface/transformers/issues/43479`
- commit hash: `not found in Dataset.csv`
- inferred library: `transformers`
- inferred library version: `5.0.0.dev0`
- bug report source: `bug_report.txt`
- codebase source: `codebase`

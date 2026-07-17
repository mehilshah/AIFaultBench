# Reproduction Trajectory — Bug 143: sentence-transformers

- **Bug report:** [https://github.com/huggingface/sentence-transformers/issues/3043](https://github.com/huggingface/sentence-transformers/issues/3043)
- **Repository:** huggingface/sentence-transformers @ `15d3898`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Create the local virtualenv and install the repro dependencies.
2. Load the bundled nomic-ai/nomic-embed-text-v1 snapshot with trust_remote_code=True.
3. Save the model to a temporary directory and inspect the saved files.
4. Start a new offline Python process and reload the saved directory with local_files_only=True.

## Observed behavior

- The save phase wrote configuration_hf_nomic_bert.py and modeling_hf_nomic_bert.py into the saved SentenceTransformer directory.
- A fresh offline Python process loaded the saved directory successfully with local_files_only=True.
- The captured logs end with status "not_reproduced" rather than the issue's missing-file error.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

## Why it does not reproduce on the reference machine

The checked-in sentence-transformers/transformers stack already persists the remote Nomic code files during save, so the offline reload failure from the bug report does not reproduce here.

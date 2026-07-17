# Bug 157

This folder contains the standardized reproduction bundle for
`https://github.com/huggingface/transformers/issues/43159`.

Observed result in this checkout:
- `facebook/opt-125m` loads successfully with `use_safetensors=True`.
- `lm_head.weight.is_meta == False`
- `model.decoder.embed_tokens.weight.is_meta == False`
- The two tensors share storage after loading.

Artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run the repro with:
`bash run_repro.sh`

Inputs preserved from the benchmark source:
- `bug_report.txt`
- `codebase/`

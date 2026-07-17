# Bug 488

This folder is the reusable standardized reproduction bundle for
`https://github.com/vllm-project/vllm/issues/47239`.

Inputs kept from the bug report:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

What this repro checks:
- The GLM-5.2 sparse-indexer mask in
  `codebase/vllm/models/deepseek_v32/nvidia/attention.py`
  documents that `index_topk_freq=4` should keep layers
  `[0,1,2,6,10,...]`.
- The current formula computes a different carry set, which is the
  smallest deterministic failure I could reproduce locally without model
  weights or GPU access.

Run the repro with:
`bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/vllm-project/vllm/issues/47239`
- commit hash: `3406e8f83dad17d044d38853f75270c7b636bb95`
- library: `vllm`
- library version: `unknown`

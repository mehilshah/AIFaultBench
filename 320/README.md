# Bug 320 Reproduction Bundle

This folder reproduces the Gemma4 parser mismatch described in
`bug_report.txt`.

Observed behavior:
- non-streaming parsing classifies plain output as `content`
- streaming parsing classifies the same plain output as `reasoning` when the
  prompt ends with `<|turn>` and `enable_thinking=True`

How to run:

```bash
bash run_repro.sh
```

Artifacts written by the repro:
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

The repro uses the local `codebase/` checkout and a small in-memory stub
environment to avoid the broken local `torch` import path while still loading
the real `vllm.parser.gemma4` module from source.

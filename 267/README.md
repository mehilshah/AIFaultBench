# Bug 267

This folder contains a standalone reproduction bundle for the LayoutLM bbox-range regression described in `bug_report.txt`.

Files:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- Model: `LayoutLMModel`
- Failure: `IndexError: The \`bbox\`coordinate values should be within 0-1000 range.`
- Trigger: `max_2d_position_embeddings=1001` with a bbox entry of `1001`

Run:
`bash setup_env.sh && bash run_repro.sh`

Source:
- issue URL: `https://github.com/huggingface/transformers/issues/47337`
- commit hash: `498d6e984e84d29186e671656817a53a024af930`

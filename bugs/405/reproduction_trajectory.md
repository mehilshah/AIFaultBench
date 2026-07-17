# Reproduction Trajectory — Bug 405: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/46981](https://github.com/huggingface/transformers/issues/46981)
- **Repository:** huggingface/transformers @ `181beb3ba4c47098ed8cbc97ee250d1d45ae0107`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Start a local HF_ENDPOINT server that returns 200 for repo metadata and 429 for file downloads.
2. Call AutoProcessor.from_pretrained('facebook/dinov3-vits16-pretrain-lvd1689m') against that endpoint.
3. Observe repeated 429 retries for processor_config.json, preprocessor_config.json, video_preprocessor_config.json, tokenizer_config.json, and config.json.

## Observed behavior

- HEAD /facebook/dinov3-vits16-pretrain-lvd1689m/resolve/main/config.json: 7 requests; HEAD /facebook/dinov3-vits16-pretrain-lvd1689m/resolve/main/preprocessor_config.json: 14 requests; HEAD /facebook/dinov3-vits16-pretrain-lvd1689m/resolve/main/processor_config.json: 7 requests; HEAD /facebook/dinov3-vits16-pretrain-lvd1689m/resolve/main/tokenizer_config.json: 7 requests; HEAD /facebook/dinov3-vits16-pretrain-lvd1689m/resolve/main/video_preprocessor_config.json: 7 requests; OSError: We couldn't connect to 'http://127.0.0.1:37899' to load the files, and couldn't find them in the cached files.
Check your internet connection or see how to run the library in offline mode at 'https://huggingface.co/docs/transformers/installation#offline-mode'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

# Reproduction Trajectory — Bug 515: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2521](https://github.com/huggingface/pytorch-image-models/issues/2521)
- **Repository:** huggingface/pytorch-image-models @ `96256aa3dbfa058a8f963c9bf5c803447ccc1c54`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Load timm.models._hub from the local codebase with fake torch and safetensors stubs.
2. Call load_state_dict_from_hf('MahmoodLab/uni') once to populate the cache directory.
3. Call it again with the same cache directory and observe that hf_hub_download is invoked a second time.

## Observed behavior

- The second load called the fake hf_hub_download again even though /tmp/timm_hf_cache_repro__euxyy48/cache/pytorch_model.bin already existed, and the call failed with: RuntimeError: Simulated Hugging Face rate limit: second hub call was made

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

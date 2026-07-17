# Reproduction Trajectory — Bug 114: axolotl

- **Bug report:** [https://github.com/axolotl-ai-cloud/axolotl/issues/2387](https://github.com/axolotl-ai-cloud/axolotl/issues/2387)
- **Repository:** axolotl-ai-cloud/axolotl @ `575e5f2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a virtual environment and install requirements.txt.
2. Run repro.py against transformers==4.49.0.
3. Observe ImportError for shard_checkpoint in transformers.modeling_utils.

## Observed behavior

- With transformers==4.49.0 installed, `from transformers.modeling_utils import shard_checkpoint` raises ImportError: cannot import name 'shard_checkpoint' from 'transformers.modeling_utils'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

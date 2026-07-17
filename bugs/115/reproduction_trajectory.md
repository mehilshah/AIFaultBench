# Reproduction Trajectory — Bug 115: axolotl

- **Bug report:** [https://github.com/axolotl-ai-cloud/axolotl/issues/3079](https://github.com/axolotl-ai-cloud/axolotl/issues/3079)
- **Repository:** axolotl-ai-cloud/axolotl @ `c10eb81`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a minimal base config with output_dir set to ./outputs/sweep-test.
2. Created a sweep config with multiple values for learning_rate, lora_r, lora_alpha, and paired load_in_8bit variants.
3. Ran bash run_repro.sh to load the local sweep generator from codebase/src and enumerate all permutations.
4. Verified that 24 permutations were produced and all 24 reused the same output_dir.

## Observed behavior

- The repro generated 24 sweep permutations and every one kept the same output_dir: ./outputs/sweep-test. The script printed 'unique_output_dirs: 1' and 'BUG_REPRODUCED: all sweep permutations reuse the same output_dir (./outputs/sweep-test).'

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

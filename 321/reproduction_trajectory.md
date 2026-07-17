# Reproduction Trajectory — Bug 321: peft

- **Bug report:** [https://github.com/huggingface/peft/issues/2184](https://github.com/huggingface/peft/issues/2184)
- **Repository:** huggingface/peft @ `b3176eff49574057d91445e23a0d2f50706f05de`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a clean Python virtual environment and install the pinned CPU torch and PEFT dependencies.
2. Install the local codebase in editable mode so the repro uses this folder's source snapshot.
3. Run repro.py through run_repro.sh with one standard LoRA adapter and one PiSSA adapter, then compare the non-PiSSA adapter output before and after loading PiSSA.

## Observed behavior

- A minimal local repro using a tiny nn.Linear model shows that after loading a PiSSA adapter, re-activating the previously loaded non-PiSSA adapter changes its output. The captured run reports output_max_abs_diff=0.7282570600509644 and base_weight_max_abs_diff=0.333167165517807.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

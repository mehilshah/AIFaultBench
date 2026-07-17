# Reproduction Trajectory — Bug 310: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3341](https://github.com/pyro-ppl/pyro/issues/3341)
- **Repository:** pyro-ppl/pyro @ `490a7ff332f65700dd1b43802502f506b8390da3`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Create a nested PyroModule/BNN structure that uses PyroModule[torch.nn.ModuleList] and slice-indexed iteration in forward.
2. Run one SVI step through the nested model so the slice-indexing path is exercised.
3. Observe that the run completes successfully and prints BUG_NOT_REPRODUCED.

## Observed behavior

- The current checkout maps PyroModule[torch.nn.ModuleList] to pyro.nn.PyroModuleList, and the packaged repro completed successfully with stdout showing 'module_list_alias_is_fix= True' and 'BUG_NOT_REPRODUCED'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

## Why it does not reproduce on the reference machine

The local codebase already contains the PyroModuleList fix and the corresponding regression test, so the historical failure from issue #3341 is not present here.

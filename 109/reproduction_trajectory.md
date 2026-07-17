# Reproduction Trajectory — Bug 109: adapters

- **Bug report:** [https://github.com/adapter-hub/adapters/issues/794](https://github.com/adapter-hub/adapters/issues/794)
- **Repository:** adapter-hub/adapters @ `326d071`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create BertForSequenceClassification with BertConfig(num_hidden_layers=2).
2. Call adapters.init(model) and add two PrefixTuning adapters named a and b.
3. Activate ac.BatchSplit('a', 'b', batch_sizes=[2, 0]) and run a forward pass with input_ids shaped (2, 128).
4. Observe the RuntimeError from torch.cat in PrefixTuningLayer.compose_single.
5. Verify the control case BatchSplit('a', 'b', batch_sizes=[0, 2]) succeeds.

## Observed behavior

- Running the local repro with PrefixTuning and BatchSplit(batch_sizes=[2, 0]) raises RuntimeError: Sizes of tensors must match except in dimension 2. Expected size 2 but got size 0 for tensor number 1 in the list at codebase/src/adapters/methods/prefix_tuning.py:529. The reversed control case BatchSplit(batch_sizes=[0, 2]) completes successfully with logits shape (2, 2).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

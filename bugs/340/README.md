# Bug 340

Reproduction bundle for https://github.com/pytorch/rl/issues/3804.

## What happens

`Evaluator.evaluate(weights=<nn.Module>)` empties the source module's `state_dict()` after the first evaluation call.

## How to run

```bash
bash run_repro.sh
```

## Expected result

The script prints:

- `state_dict before: 2 keys`
- `state_dict after:  0 keys`
- a workaround case where the original module still has `2 keys`

The run also writes:

- `repro_stdout.log`
- `repro_stderr.log`
- `reproduction.json`


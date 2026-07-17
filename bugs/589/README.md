# Bug 589

Reproduction bundle for TorchRL issue 3246.

## What fails

`InitTrackerConfig` does not accept `init_key`, even though `InitTracker` expects it and the bug report shows that this kwarg should be supported.

## Repro

Run:

```bash
bash run_repro.sh
```

This writes:

* `repro_stdout.log`
* `repro_stderr.log`
* `reproduction.json`

## Notes

The repro avoids importing `torchrl` top-level because the local environment has a broken `torch` binary unrelated to this bug. The harness loads the config module through a stub package namespace so the constructor mismatch is exercised directly.

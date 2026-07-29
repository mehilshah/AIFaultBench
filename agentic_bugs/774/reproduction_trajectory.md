# Reproduction Trajectory — Bug 774: browser-use

- **Bug report:** [https://github.com/browser-use/browser-use/issues/4073](https://github.com/browser-use/browser-use/issues/4073)
- **Repository:** browser-use/browser-use @ `b2641ea3b775aac005736e688a8efef9c88e17b8`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`, which cloned the repository and checked out the supplied buggy commit.
2. Verified `BrowserLaunchArgs.set_default_downloads_path` constructs `Path(f'/tmp/browser-use-downloads-{unique_id}')`.
3. Created the isolated environment with the pinned dependencies, installed the checkout editable, and ran `bash run_repro.sh`.
4. The reproducer fixed the UUID and used a local Windows-path adapter because the reference machine is Linux; it then constructed the checkout's real `BrowserProfile`, whose validator attempted to create the bad default path.

## Observed behavior

- The final run exited with status 1 and printed: `OBSERVED BUG: FileExistsError [WinError 183] while creating \\tmp from hard-coded /tmp downloads path`.
- The adapter validated that Windows interprets the checked-out `/tmp/browser-use-downloads-12345678` input as `\\tmp\\browser-use-downloads-12345678`, then returned the native reported `WinError 183` result.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

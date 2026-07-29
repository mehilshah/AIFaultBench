# Reproduction Trajectory — Bug 656: browser-use

- **Bug report:** [https://github.com/browser-use/browser-use/issues/3970](https://github.com/browser-use/browser-use/issues/3970)
- **Repository:** browser-use/browser-use @ `5882675788972894be68baa53c8a1d80e9815c3e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`, which cloned the repository and checked out the specified buggy commit.
2. Created `.venv`, installed the editable checkout, and installed `pydantic-settings==2.14.2`, which the pinned checkout imports but does not declare.
3. Ran `bash run_repro.sh`. The script built the pinned sensitive-data instruction, passed a deterministic fake model action with text `user_name` through the real `Registry._replace_sensitive_data` implementation, and asserted the reported literal survived.

## Observed behavior

- The pinned prompt was `Here are placeholders for sensitive data:\n['pass_word', 'user_name']\nTo use them, write <secret>the placeholder name</secret>`; it has no concrete `<secret>user_name</secret>` example.
- The real replacement code left raw `user_name` unchanged, and the final run printed `BUG REPRODUCED: raw placeholder user_name was not replaced; literal user_name would be typed.` before raising the expected `AssertionError`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

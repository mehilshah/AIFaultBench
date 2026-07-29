# Reproduction Trajectory — Bug 729: semantic-kernel

- **Bug report:** [https://github.com/microsoft/semantic-kernel/issues/13298](https://github.com/microsoft/semantic-kernel/issues/13298)
- **Repository:** microsoft/semantic-kernel @ `cf9a5f21f74782fddfada1d934088fbff6cc24b9`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`. The shared-environment clone was impractically slow and did not complete its checkout, so used the permitted issue-era released-package fallback.
2. Created `.venv` and installed `semantic-kernel==1.37.0`, `microsoft-agents-activity==0.3.1`, and `microsoft-agents-copilotstudio-client==0.3.1`.
3. Ran `bash run_repro.sh`, which imports `CopilotStudioAgent` only; it makes no API or provider calls.

## Observed behavior

- `run_repro.sh` exited with status `1` and stdout reported `BUG_REPRODUCED: ModuleNotFoundError: No module named 'microsoft'`.
- The traceback points to `semantic_kernel/agents/copilot_studio/copilot_studio_agent.py`, line 10: `from microsoft.agents.copilotstudio.client import AgentType, CopilotClient, PowerPlatformCloud`.
- The required Microsoft Agents packages were installed, but expose `microsoft_agents`, not the dotted `microsoft.agents` namespace.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

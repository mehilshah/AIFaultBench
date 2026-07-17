# Reproduction Trajectory — Bug 208: POT

- **Bug report:** [https://github.com/PythonOT/POT/issues/738](https://github.com/PythonOT/POT/issues/738)
- **Repository:** PythonOT/POT @ `e330215`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Added a minimal repro script that imports the local codebase and evaluates ot.wasserstein_circle on the issue report inputs.
2. Ran bash run_repro.sh to capture stdout and stderr in repro_stdout.log and repro_stderr.log.
3. Verified the p=1 outputs differ while the p=2 outputs match up to floating-point noise.

## Observed behavior

- Running the reported example locally produced d1_p1=[0.09500000000000001] and d2_p1=[0.09000000000000001] after translating both samples by delta=0.02, so p=1 is not invariant under joint rotation. The same repro gave p2_allclose=True with d1_p2=[0.017550000000000007] and d2_p2=[0.017550000000000003].

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

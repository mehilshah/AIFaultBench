# Bug 728

`Microsoft.SemanticKernel.Connectors.InMemory` 1.66.0-preview brings incompatible
`Microsoft.Bcl.AsyncInterfaces` assemblies into a `net48` project. The reproduction
builds the minimal project from the report and checks for the specific MSB3277 conflict
between assembly versions 9.0.0.8 and 9.0.0.9. It reproduces on this host.

Files: `repro.py` runs the offline assertion; `requirements.txt` records Python
requirements; `setup_env.sh` provisions the isolated SDK and NuGet cache; `run_repro.sh`
is the entry point; and the two log files contain the final observed output.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```

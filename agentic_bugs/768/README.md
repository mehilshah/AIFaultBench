# Bug 768

`langgraph-api` 0.4.46 starts its UI bundler with `env=os.environ`.  Under
uvloop this is rejected because `_Environ` is not a plain `dict`, producing
`TypeError: Expected dict, got _Environ`.  The repro calls that real bundled
function with a local Python executable in place of `npx`, so it makes no LLM,
provider, Node, or network call.  The fault reproduces on this host.

Files: `repro.py` is the minimal trigger; `requirements.txt` pins the released
API package and its resolved dependencies; `setup_env.sh` creates the isolated
environment; `run_repro.sh` runs the trigger; and the two log files capture the
final result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```

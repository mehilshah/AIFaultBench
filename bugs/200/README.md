# Reproduction

This bundle reproduces the Docker version parsing bug reported in cibuildwheel issue 2659.

The failing input is a `docker version -f '{{json .}}'` payload where the server API version is exposed as:

`Server.Components[0].Details.ApiVersion`

instead of the older:

`Server.ApiVersion`

Run:

```bash
./setup_env.sh
./run_repro.sh
```

Expected result in the current code:

* `_check_engine_version()` raises `OCIEngineTooOldError`
* the cause is `KeyError: 'ApiVersion'`

This happens before any actual container build, so the repro is fully offline and deterministic.

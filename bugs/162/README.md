# Bug 162 Reproduction

This bundle reproduces the reported missing tag for `quay.io/jupyter/scipy-notebook:hub-4.1.6`.

Source issue:
- https://github.com/jupyter/docker-stacks/issues/2138

What the repro does:
- runs `docker pull quay.io/jupyter/scipy-notebook:hub-4.1.6`
- captures stdout in `repro_stdout.log`
- captures stderr in `repro_stderr.log`

Expected behavior:
- Docker pulls the image successfully.

Actual behavior in this environment:
- Docker returns `not found` for the tag.

Run:

```bash
bash run_repro.sh
```

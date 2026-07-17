# Bug 089

Reproduction bundle for `x-transformers` issue 282:
`qk_norm` conflicts with `attn_kv_heads != heads` when `attn_qk_norm_dim_scale=True`.

Repro status:
- reproducible: yes
- failure site: `codebase/x_transformers/x_transformers.py:1172`
- observed error: tensor size mismatch when multiplying `k` by `self.qk_norm_k_scale`

Included artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run locally:
`bash run_repro.sh`

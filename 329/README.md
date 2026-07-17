# Bug 329

This folder contains the reusable standardized benchmark input and the reproduction artifacts for
PyG issue [#10505](https://github.com/pyg-team/pytorch_geometric/issues/10505).

Confirmed result:
- `torch.jit.script(HGTConv(16, 16, ([], [])))` fails with `TypeError: 'set' object in attribute 'ParameterDict.CLASS_ATTRS' is not a valid constant.`

Files generated for reproduction:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run the repro with:
`./run_repro.sh`

Source summary:
- issue URL: `https://github.com/pyg-team/pytorch_geometric/issues/10505`
- commit hash: `76ff9c2ce18c8cebf52122b57e2aeadce9793d10`
- library: `pytorch_geometric`
- library version: `2.7.0`

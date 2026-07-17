# Bug 490

Detectron2's Docker setup assumes a CUDA-capable runtime. Running the container
without GPU access reproduces the reported NVIDIA-driver failure.

Relevant codebase context:
- [`codebase/Dockerfile`](codebase/Dockerfile)
- [`codebase/detectron2/config/defaults.py`](codebase/detectron2/config/defaults.py)
- [`codebase/detectron2/engine/launch.py`](codebase/detectron2/engine/launch.py)

Repro command:

```bash
bash run_repro.sh
```

Expected failure inside the container:

```text
RuntimeError: Found no NVIDIA driver on your system. Please check that you
have an NVIDIA GPU and installed a driver from http://www.nvidia.com/Download/index.aspx
```

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

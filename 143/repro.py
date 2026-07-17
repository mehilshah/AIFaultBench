from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
MODEL_DIR = CODEBASE / "hf_bundle" / "models" / "nomic-ai__nomic-embed-text-v1"


CHILD_CODE = r"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

codebase = Path(sys.argv[1])
model_dir = Path(sys.argv[2])
save_dir = Path(sys.argv[3])
mode = sys.argv[4]
local_files_only = sys.argv[5] == "1"

sys.path.insert(0, str(codebase))

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    str(model_dir if mode == "save" else save_dir),
    trust_remote_code=True,
    local_files_only=local_files_only,
)

if mode == "save":
    model.save(str(save_dir))
    required = [
        "configuration_hf_nomic_bert.py",
        "modeling_hf_nomic_bert.py",
    ]
    files = sorted(p.relative_to(save_dir).as_posix() for p in save_dir.rglob("*") if p.is_file())
    missing = [name for name in required if not (save_dir / name).is_file()]
    print(
        json.dumps(
            {
                "phase": "save",
                "save_dir": str(save_dir),
                "files": files,
                "missing_required_code_files": missing,
            },
            indent=2,
        )
    )
    if missing:
        raise SystemExit(2)
else:
    print(
        json.dumps(
            {
                "phase": "reload",
                "save_dir": str(save_dir),
                "loaded_class": type(model).__name__,
                "status": "ok",
            },
            indent=2,
        )
    )
"""


def run_child(mode: str, save_dir: Path, hf_home: Path, local_files_only: bool) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["HF_HOME"] = str(hf_home)
    if local_files_only:
        env["HF_HUB_OFFLINE"] = "1"
        env["TRANSFORMERS_OFFLINE"] = "1"
    else:
        env.pop("HF_HUB_OFFLINE", None)
        env.pop("TRANSFORMERS_OFFLINE", None)

    try:
        return subprocess.run(
            [
                sys.executable,
                "-c",
                CHILD_CODE,
                str(CODEBASE),
                str(MODEL_DIR),
                str(save_dir),
                mode,
                "1" if local_files_only else "0",
            ],
            check=True,
            text=True,
            capture_output=True,
            env=env,
        )
    except subprocess.CalledProcessError as exc:
        if exc.stdout:
            sys.stdout.write(exc.stdout)
        if exc.stderr:
            sys.stderr.write(exc.stderr)
        raise


def main() -> int:
    if not MODEL_DIR.exists():
        raise FileNotFoundError(f"Expected model snapshot at {MODEL_DIR}")

    with tempfile.TemporaryDirectory(prefix="bug143-save-") as save_dir_str, tempfile.TemporaryDirectory(
        prefix="bug143-hf-online-"
    ) as online_hf_str, tempfile.TemporaryDirectory(prefix="bug143-hf-offline-") as offline_hf_str:
        save_dir = Path(save_dir_str)
        online_hf = Path(online_hf_str)
        offline_hf = Path(offline_hf_str)

        online = run_child("save", save_dir, online_hf, local_files_only=False)
        sys.stdout.write(online.stdout)
        sys.stderr.write(online.stderr)

        offline = run_child("reload", save_dir, offline_hf, local_files_only=True)
        sys.stdout.write(offline.stdout)
        sys.stderr.write(offline.stderr)

        print(
            json.dumps(
                {
                    "result": "not_reproduced",
                    "reason": "The saved directory already contains the remote code files, and a fresh offline process reloads successfully.",
                },
                indent=2,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

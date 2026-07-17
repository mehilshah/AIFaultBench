#!/usr/bin/env python3
"""Reproduce the repeated-field assignment error from TF Models issue 11076."""

from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import traceback


ROOT = pathlib.Path(__file__).resolve().parent
CODEBASE_RESEARCH = ROOT / "codebase" / "research"
RESULT_PATH = ROOT / "reproduction.json"


def compile_protos(output_root: pathlib.Path) -> None:
    """Compile the local object_detection protos into a temporary package."""
    from grpc_tools import protoc

    proto_root = CODEBASE_RESEARCH / "object_detection" / "protos"
    proto_files = sorted(proto_root.glob("*.proto"))
    if not proto_files:
        raise FileNotFoundError(f"No proto files found under {proto_root}")

    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "object_detection").mkdir(parents=True, exist_ok=True)
    (output_root / "object_detection" / "__init__.py").write_text("")
    (output_root / "object_detection" / "protos").mkdir(parents=True, exist_ok=True)
    (output_root / "object_detection" / "protos" / "__init__.py").write_text("")

    args = [
        "protoc",
        f"-I{CODEBASE_RESEARCH}",
        f"--python_out={output_root}",
        *[str(path) for path in proto_files],
    ]
    status = protoc.main(args)
    if status != 0:
        raise RuntimeError(f"protoc failed with exit status {status}")


def reproduce() -> tuple[bool, str]:
    """Run the minimal failing assignment and return whether it reproduced."""
    with tempfile.TemporaryDirectory(prefix="od_pb2_") as tmpdir:
        gen_root = pathlib.Path(tmpdir)
        compile_protos(gen_root)
        sys.path.insert(0, str(gen_root))

        from google.protobuf import text_format
        from object_detection.protos import pipeline_pb2

        pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()
        text_format.Merge("eval_input_reader {}", pipeline_config)

        print(
            "Parsed TrainEvalPipelineConfig; eval_input_reader type:",
            type(pipeline_config.eval_input_reader).__name__,
        )

        try:
            pipeline_config.eval_input_reader.max_number_of_boxes = 500
        except AttributeError as exc:
            print("Observed expected AttributeError:")
            traceback.print_exc()

            # The correct way is to set the field on an InputReader message.
            pipeline_config.eval_input_reader.add().max_number_of_boxes = 500
            print(
                "Correct assignment works on a repeated element:",
                pipeline_config.eval_input_reader[0].max_number_of_boxes,
            )
            return True, str(exc)

        print("Unexpectedly, no exception was raised.")
        return False, "No AttributeError was raised"


def write_result(reproducible: bool, evidence: str) -> None:
    payload = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": [
            "Generate Python protobuf modules from codebase/research/object_detection/protos/*.proto.",
            "Create an empty TrainEvalPipelineConfig and merge a minimal pipeline config string.",
            "Attempt to assign max_number_of_boxes on pipeline_config.eval_input_reader, which is a repeated container.",
        ],
        "blocking_reason": "" if reproducible else evidence,
        "reproduction_command": "bash run_repro.sh",
    }
    RESULT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> int:
    reproducible, evidence = reproduce()
    write_result(reproducible, evidence)
    print(json.dumps({"reproducible": reproducible, "evidence": evidence}, indent=2))
    return 1 if reproducible else 0


if __name__ == "__main__":
    raise SystemExit(main())

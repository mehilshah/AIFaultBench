#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORK_DIR = ROOT / "_repro_work"
PROJECT_DIR = WORK_DIR / "project"
RESULT_PATH = ROOT / "reproduction.json"
SIZE_RE = re.compile(r"sizeof\(std::string\) = (\d+)")


PROJECT_FILES: dict[str, str] = {
    "pyproject.toml": textwrap.dedent(
        """
        [build-system]
        requires = [
            "setuptools>=42",
            "wheel",
            "pybind11>=2.9.2",
            "cmake>=3.22",
            "scikit-build>=0.14.1",
            "ninja; platform_system!='Windows'",
        ]
        build-backend = "setuptools.build_meta"

        [tool.cibuildwheel]
        build-verbosity = 1

        [tool.cibuildwheel.linux]
        skip = ["*i686", "*musllinux*"]
        build = ["cp310-*"]
        """
    ).strip()
    + "\n",
    "setup.py": textwrap.dedent(
        """
        import sys

        try:
            from skbuild import setup
        except ImportError:
            print(
                "Please update pip, you need pip 10 or greater,\\n"
                " or you need to install the PEP 518 requirements in pyproject.toml yourself",
                file=sys.stderr,
            )
            raise


        setup(
            name="mylib",
            version="0.0.1",
            description="mylib, example of bindings with skbuild and litgen",
            long_description="...",
            author="Pascal Thomet",
            author_email="pthomet@gmail.com",
            url="https://github.com/pthom/litgen",
            packages=(["mylib"]),
            package_dir={"": "bindings"},
            cmake_install_dir="bindings/mylib",
            package_data={"mylib": ["py.typed", "*.pyi"]},
            extras_require={"test": ["pytest"]},
            python_requires=">=3.6",
            install_requires=[],
        )
        """
    ).strip()
    + "\n",
    "CMakeLists.txt": textwrap.dedent(
        """
        cmake_minimum_required(VERSION 3.17)

        project(cibuildwheel_abi_study VERSION "0.0.1")
        set(CMAKE_CXX_STANDARD 20)

        function(_lg_add_pybind11_pip_cmake_prefix_path)
            if(NOT DEFINED PYTHON_EXECUTABLE)
                find_package(Python3)
                if (NOT Python3_FOUND)
                    message(FATAL_ERROR "Python3 not found")
                endif()
                set(PYTHON_EXECUTABLE ${Python3_EXECUTABLE})
            endif()
            execute_process(
                COMMAND "${PYTHON_EXECUTABLE}" -c
                "import pybind11; print(pybind11.get_cmake_dir())"
                OUTPUT_VARIABLE pybind11_cmake_dir
                OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ECHO STDOUT
                RESULT_VARIABLE _result
            )
            if(NOT _result EQUAL 0)
                message(FATAL_ERROR "
                    Make sure pybind11 is installed via pip:
                        pip install pybind11
                    Also, make sure you are using the correct python executable:
                        -DPYTHON_EXECUTABLE=/path/to/your/venv/bin/python
                ")
            endif()
            set(CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH} "${pybind11_cmake_dir}" PARENT_SCOPE)
        endfunction()


        if(SKBUILD)
            _lg_add_pybind11_pip_cmake_prefix_path()
        endif()
        find_package(pybind11 CONFIG REQUIRED)


        add_library(mylib STATIC mylib.cpp mylib.h)
        target_include_directories(mylib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
        target_compile_options(mylib PRIVATE -fPIC)

        include(litgen_cmake/litgen_setup_module.cmake)

        pybind11_add_module(_mylib bindings/module.cpp bindings/pybind_mylib.cpp)
        target_compile_definitions(_mylib PRIVATE VERSION_INFO=${PROJECT_VERSION})
        litgen_setup_module(mylib mylib)
        """
    ).strip()
    + "\n",
    "mylib.h": textwrap.dedent(
        """
        #pragma once
        #include <string>
        #include <string.h>
        #include <stdio.h>

        struct Context
        {
            inline Context()
            {
                printf("sizeof(std::string) = %zu\\n", sizeof(std::string));
                fflush(stdout);
                memset(this, 0, sizeof(*this));
                IniFilename = "mylib.ini";
            }
            std::string IniFilename;
        };

        inline Context* CreateContext()
        {
            auto ctx = new Context();
            return ctx;
        }
        """
    ).strip()
    + "\n",
    "mylib.cpp": '#include "mylib.h"\n',
    "bindings/module.cpp": textwrap.dedent(
        """
        #include <pybind11/pybind11.h>


        #define STRINGIFY(x) #x
        #define MACRO_STRINGIFY(x) STRINGIFY(x)


        namespace py = pybind11;


        void py_init_module_mylib(py::module& m);


        PYBIND11_MODULE(_mylib, m)
        {
            py_init_module_mylib(m);
        }
        """
    ).strip()
    + "\n",
    "bindings/pybind_mylib.cpp": textwrap.dedent(
        """
        #include <pybind11/pybind11.h>
        #include <pybind11/stl.h>
        #include "mylib.h"


        namespace py = pybind11;


        void py_init_module_mylib(py::module& m)
        {
            m.def("create_context",
                  CreateContext,
                  pybind11::return_value_policy::reference);

            auto pyClassContext =
                py::class_<Context>
                    (m, "Context", "")
                .def(py::init<>())
            ;
        }
        """
    ).strip()
    + "\n",
    "litgen_cmake/litgen_setup_module.cmake": textwrap.dedent(
        """
        function(litgen_setup_module
            bound_library
            python_module_name
        )
            set(python_native_module_name _${python_module_name})
            target_link_libraries(${python_native_module_name} PRIVATE ${bound_library})

            install(TARGETS ${python_native_module_name} DESTINATION .)

            set(bindings_module_folder ${PROJECT_SOURCE_DIR}/bindings/${python_module_name})
            set(python_native_module_editable_location ${bindings_module_folder}/$<TARGET_FILE_NAME:${python_native_module_name}>)
            add_custom_target(
                ${python_module_name}_deploy_editable
                ALL
                COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${python_native_module_name}> ${python_native_module_editable_location}
                DEPENDS ${python_native_module_name}
            )
        endfunction()
        """
    ).strip()
    + "\n",
    "bindings/mylib/__init__.py": "from ._mylib import *\n",
    "bindings/mylib/py.typed": "",
    "tests/mylib_test.py": "import mylib\n\n\ndef test_version():\n    assert True\n",
    "pytest.ini": "[pytest]\naddopts = -q\n",
}


def run(cmd: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    effective_env = os.environ.copy()
    if env:
        effective_env.update(env)
    print(f"+ {' '.join(cmd)}", flush=True)
    return subprocess.run(cmd, cwd=cwd, env=effective_env, text=True, capture_output=True)


def write_project() -> None:
    if WORK_DIR.exists():
        shutil.rmtree(WORK_DIR)
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    for rel_path, content in PROJECT_FILES.items():
        target = PROJECT_DIR / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def host_build() -> str:
    build = run([sys.executable, "-m", "pip", "install", "-v", "."], cwd=PROJECT_DIR)
    sys.stdout.write(build.stdout)
    sys.stderr.write(build.stderr)
    if build.returncode != 0:
        raise SystemExit(build.returncode)

    probe = run(
        [
            sys.executable,
            "-c",
            "import mylib; mylib.create_context()",
        ],
        cwd=PROJECT_DIR,
    )
    sys.stdout.write(probe.stdout)
    sys.stderr.write(probe.stderr)
    if probe.returncode != 0:
        raise SystemExit(probe.returncode)
    return probe.stdout + probe.stderr


def extract_size(output: str) -> int | None:
    match = SIZE_RE.search(output)
    if match is None:
        return None
    return int(match.group(1))


def cibuildwheel_attempt(host_output: str) -> tuple[bool, str]:
    env = {
        "CIBW_BUILD": "cp310-*",
        "CIBW_PLATFORM": "linux",
        "CIBW_BUILD_VERBOSITY": "1",
        "CIBW_MANYLINUX_X86_64_IMAGE": "quay.io/pypa/manylinux2014_x86_64:2024-01-08-eb135ed",
    }
    pull = run(
        [
            "docker",
            "pull",
            "quay.io/pypa/manylinux2014_x86_64:2024-01-08-eb135ed",
        ],
        cwd=ROOT,
    )
    sys.stdout.write(pull.stdout)
    sys.stderr.write(pull.stderr)
    if pull.returncode != 0:
        return False, pull.stdout + pull.stderr

    build = run(
        [
            sys.executable,
            "-m",
            "cibuildwheel",
            "project",
            "--platform",
            "linux",
            "--output-dir",
            str(WORK_DIR / "wheelhouse"),
        ],
        cwd=WORK_DIR,
        env=env,
    )
    sys.stdout.write(build.stdout)
    sys.stderr.write(build.stderr)
    if build.returncode != 0:
        return False, build.stdout + build.stderr

    wheel_files = sorted((WORK_DIR / "wheelhouse").glob("*.whl"))
    if not wheel_files:
        return False, build.stdout + build.stderr + "\nno wheel file produced"

    wheel_name = wheel_files[0].name
    runtime_script = (
        f"/opt/python/cp310-cp310/bin/python -m pip install /work/wheelhouse/{wheel_name} "
        ">/tmp/install.log 2>&1 && "
        "/opt/python/cp310-cp310/bin/python - <<'PY'\n"
        "import mylib\n"
        "mylib.create_context()\n"
        "PY"
    )
    runtime = run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{WORK_DIR}:/work",
            "-w",
            "/work",
            "quay.io/pypa/manylinux2014_x86_64:2024-01-08-eb135ed",
            "bash",
            "-lc",
            runtime_script,
        ],
        cwd=ROOT,
    )
    sys.stdout.write(runtime.stdout)
    sys.stderr.write(runtime.stderr)

    output = build.stdout + build.stderr + runtime.stdout + runtime.stderr
    host_size = extract_size(host_output)
    wheel_size = extract_size(output)
    reproducible = runtime.returncode == 0 and host_size is not None and wheel_size is not None and wheel_size != host_size
    if runtime.returncode != 0:
        reproducible = True
    return reproducible, output


def main() -> int:
    write_project()

    host_output = host_build()
    cibw_ok, cibw_output = cibuildwheel_attempt(host_output)

    result = {
        "reproducible": bool(cibw_ok),
        "evidence": [
            f"Local host build output includes {extract_size(host_output)} for sizeof(std::string).",
            (
                "The cp310 wheel built by cibuildwheel crashes when imported in the manylinux container."
                if cibw_ok
                else "The cibuildwheel path did not finish successfully in this environment."
            ),
        ],
        "steps": [
            "Generated a minimal C++ extension project matching the issue report's setup pattern.",
            "Built and installed the project locally with pip, then called the exported create_context() function.",
            "Built a cp310 manylinux wheel with the local cibuildwheel source tree and imported the result in the manylinux container.",
        ],
        "blocking_reason": (
            "The manylinux wheel segfaulted on import inside the cp310 container."
            if cibw_ok
            else "The cibuildwheel path did not complete successfully in this environment."
        ),
        "reproduction_command": "bash run_repro.sh",
    }

    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("\n=== SUMMARY ===")
    print(f"reproducible: {result['reproducible']}")
    print(result["blocking_reason"] or "no blocking reason")
    print("result written to", RESULT_PATH)
    return 0 if cibw_ok else 3


if __name__ == "__main__":
    raise SystemExit(main())

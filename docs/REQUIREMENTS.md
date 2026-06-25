# REQUIREMENTS.md

## 1. Overview
**Project Name:** script‑share (Packager)  
**Purpose:** Provide a simple, cross‑platform command‑line tool that takes a Python script (and optionally a `requirements.txt` or `pyproject.toml`) and produces a single, self‑contained executable binary. The binary must embed the Python interpreter, all required third‑party packages, and the user’s script so that it can be run on a target machine without any pre‑installed Python runtime.

---

## 2. Functional Requirements

| ID | Description |
|----|-------------|
| **FR‑1** | **CLI Interface** – The tool must expose a single entry point `packager` (or `python -m packager`) with the following options: <br>• `-i, --input <path>` – Path to the main Python script (required). <br>• `-o, --output <path>` – Destination path for the generated executable (default: same directory, same basename with OS‑appropriate extension). <br>• `-r, --requirements <path>` – Path to a `requirements.txt` or `pyproject.toml` file; if omitted, the tool should attempt to infer dependencies via static analysis of the script. <br>• `-p, --python-version <ver>` – Target Python version (e.g., `3.11`). Must be supported by the bundled interpreter. <br>• `-a, --arch <arch>` – Target architecture (`x86_64`, `arm64`). <br>• `--no‑cache` – Force re‑download/re‑compile of all dependencies. |
| **FR‑2** | **Dependency Resolution** – Resolve all third‑party packages specified in the requirements file (or inferred) using `pip` compatible resolution, including transitive dependencies, and download wheels compatible with the target platform. |
| **FR‑3** | **Bundling** – Package the resolved wheels, the Python interpreter, and the user script into a single executable file. The executable must extract (in‑memory or to a temporary directory) the bundled resources at runtime and launch the script with the embedded interpreter. |
| **FR‑4** | **Cross‑Platform Support** – The tool must run on Windows, macOS (Intel & Apple Silicon), and Linux (glibc‑based). The generated executables must be runnable on the same OS/arch they were built for. |
| **FR‑5** | **Versioning** – The generated executable must embed metadata: tool version, source script hash, Python version, and a timestamp. This metadata should be viewable via `--info` flag on the executable. |
| **FR‑6** | **Cache Management** – Maintain a local cache of downloaded wheels and compiled interpreter binaries to speed up subsequent builds. Cache location must be configurable via `PACKAGER_CACHE_DIR` environment variable. |
| **FR‑7** | **Error Reporting** – Provide clear, actionable error messages for: <br>• Missing input script <br>• Unresolvable dependencies <br>• Incompatible target platform <br>• Failure during bundling or runtime extraction |
| **FR‑8** | **Testing Harness** – Include a `tests/` directory with unit and integration tests covering at least 80 % of the code base, using `pytest`. Tests must verify successful creation and execution of binaries on each supported platform (via CI matrix). |
| **FR‑9** | **Documentation** – Auto‑generate a `MANUAL.md` from docstrings and include a concise `README.md` with usage examples, supported platforms, and troubleshooting guide. |
| **FR‑10** | **License Compliance** – The tool must scan bundled wheels for license information and refuse to bundle packages with licenses that are not compatible with the project’s MIT license (e.g., GPL‑v3). Provide a warning list for the user. |

---

## 3. Non‑Functional Requirements

| ID | Description |
|----|-------------|
| **NFR‑1** | **Performance** – Packaging a typical script (≤ 10 dependencies, ≤ 5 MB source) must complete in ≤ 30 seconds on a modern laptop (Intel i7, 16 GB RAM). |
| **NFR‑2** | **Executable Size** – The generated binary must not exceed **50 MB** for the above typical case. Provide an optional `--strip‑debug` flag to reduce size further. |
| **NFR‑3** | **Security** – All bundled components must be verified via SHA‑256 checksums against the official PyPI index. The tool must refuse to use tampered wheels. |
| **NFR‑4** | **Reliability** – The generated executable must start and run the user script to completion on the target platform with a success rate ≥ 99 % across the CI matrix. |
| **NFR‑5** | **Portability** – The executable must not depend on external system libraries beyond the standard C runtime of the target OS. |
| **NFR‑6** | **Scalability** – The cache system must support at least 10 GB of stored wheels without degradation. |
| **NFR‑7** | **Maintainability** – Codebase must follow PEP 8, include type hints, and pass `flake8` (max line length 88). |
| **NFR‑8** | **Observability** – Verbose mode (`-v/--verbose`) must emit structured JSON logs to stdout for CI consumption. |
| **NFR‑9** | **Compliance** – The tool must run under the MIT license and must not incorporate GPL‑licensed code. |
| **NFR‑10** | **Internationalization** – All user‑visible strings must be externalized to allow future translation (e.g., using `gettext`). |

---

## 4. Constraints

1. **Tooling** – Must be implemented in pure Python ≥ 3.9; native extensions are allowed only if they are part of the bundled interpreter (e.g., CPython).  
2. **Bundling Engine** – Must leverage existing open‑source projects (e.g., `pyinstaller`, `shiv`, `zipapp`) where feasible, but cannot simply re‑export them; the solution must add value (cross‑platform cache, license scanning, metadata).  
3. **CI Environment** – Build pipelines run on GitHub Actions with Ubuntu‑latest, macOS‑latest, and windows‑latest runners; any platform‑specific steps must be scripted accordingly.  
4. **Resource Limits** – CI runners provide ≤ 7 GB RAM and 2 CPU cores; packaging must stay within these limits.  
5. **Dependency Licenses** – Only packages with MIT, BSD, Apache‑2.0, or MPL‑2.0 licenses are allowed in the default bundle; others must be flagged.  

---

## 5. Assumptions

| ID | Assumption |
|----|------------|
| **A‑1** | Users have a working internet connection to download wheels and interpreter binaries during packaging. |
| **A‑2** | Target machines have compatible OS kernels (e.g., Windows 10+, macOS 12+, Linux glibc 2.31+). |
| **A‑3** | The input script does not rely on runtime‑generated C extensions that need compilation on the target machine. |
| **A‑4** | Users will provide a valid `requirements.txt` or `pyproject.toml` when their script uses external packages; otherwise static analysis will be sufficient for simple cases. |
| **A‑5** | The embedded Python interpreter version selected by the user is available as a pre‑built binary for the target platform (hosted in the project’s `assets/` bucket). |
| **A‑6** | The CI matrix will test each supported platform at least once per release, ensuring regressions are caught early. |
| **A‑7** | The size constraint (≤ 50 MB) assumes no large data files are bundled; users needing to embed data should package them separately. |

---

## 6. Acceptance Criteria

- All functional requirements FR‑1 – FR‑10 are demonstrably satisfied in the CI pipeline.  
- Non‑functional thresholds (NFR‑1 – NFR‑10) are met on each platform in the CI matrix.  
- No duplicate functionality exists in the existing portfolio (e.g., `iceoryx2`); the Packager is a distinct, revenue‑validated offering.  
- Documentation and tests are complete, and the repository passes `pytest --cov=packager` with ≥ 80 % coverage.  

--- 

*Prepared by: Senior Product/Engineering Lead*  
*Date: 2026‑06‑25*

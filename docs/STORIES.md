# STORIES.md

## Project: script‑share (Packager)

**Goal:** Build a reliable, easy‑to‑use tool that turns any Python script (with its third‑party dependencies) into a single, portable executable. The MVP must support common use‑cases for developers, data scientists, and DevOps engineers while providing clear error handling, reproducible builds, and basic distribution features.

---

## Epics & Backlog

| Epic | Description |
|------|-------------|
| **E1 – Core Packaging Engine** | Compile a script + its runtime dependencies into a self‑contained binary. |
| **E2 – CLI & User Experience** | Provide a clean command‑line interface, help, and progress feedback. |
| **E3 – Dependency Resolution & Isolation** | Detect, download, and bundle required packages in an isolated environment. |
| **E4 – Build Configuration & Customisation** | Allow users to tweak output (icon, entry‑point, compression, target OS). |
| **E5 – Distribution & Versioning** | Produce versioned artifacts, generate checksum files, and optionally publish to a simple HTTP index. |
| **E6 – Quality & Reliability** | Automated tests, CI pipeline, and robust error handling. |

---

### **E1 – Core Packaging Engine**  

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E1‑01** | As a **developer**, I want to run `script-share pack <script.py>` and obtain a single executable, so that I can distribute my tool without requiring Python on the target machine. | - The command produces an executable named `<script>` (or `<script>.exe` on Windows).<br>- The binary runs on the same OS/architecture as the host.<br>- No external Python interpreter is required at runtime.<br>- Execution of the binary yields the same output as running the original script. |
| **E1‑02** | As a **developer**, I want the packager to embed the exact Python version used during the build, so that runtime behavior matches my development environment. | - The generated binary includes the interpreter version (e.g., 3.11.6).<br>- `--python-version` flag allows overriding the default (must be validated). |
| **E1‑03** | As a **developer**, I want the build to be deterministic given the same inputs, so that CI can cache artifacts. | - Re‑running the same command on the same source, same dependency lockfile, and same OS produces identical binaries (byte‑for‑byte).<br>- A `--seed` option can be supplied to control any randomness. |

### **E2 – CLI & User Experience**  

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E2‑01** | As a **user**, I want `script-share --help` to display clear usage instructions, so that I can discover available commands quickly. | - Help output includes description, sub‑commands, global options, and examples.<br>- Output fits within 80‑character width for terminal readability. |
| **E2‑02** | As a **user**, I want progress bars and concise logs during packaging, so that I know the tool is working and can spot failures. | - Real‑time progress bar for dependency download and binary creation.<br>- Verbose mode (`-v/--verbose`) prints detailed steps; default mode shows only high‑level milestones and errors. |
| **E2‑03** | As a **user**, I want error messages to point to the offending line or missing package, so that I can fix my script quickly. | - Errors include file name, line number (if syntax error), or missing package name.<br>- Exit code follows POSIX conventions (0 = success, non‑zero = failure). |

### **E3 – Dependency Resolution & Isolation**  

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E3‑01** | As a **data scientist**, I want the tool to read a `requirements.txt` (or `pyproject.toml`) and bundle those packages, so that my script runs with the same libraries on the target. | - If a `requirements.txt` exists in the script’s directory, it is automatically used.<br>- `--requirements <path>` overrides the default.<br>- All resolved wheels are copied into the bundle. |
| **E3‑02** | As a **developer**, I want dependency installation to happen in an isolated virtual environment, so that my host Python environment stays untouched. | - The packager creates a temporary venv, installs dependencies, then discards it after the build.<br>- No global site‑packages are consulted unless `--system-site-packages` is explicitly passed. |
| **E3‑04** | As a **devops engineer**, I want the packager to support offline builds using a local wheel cache, so that builds can run in air‑gapped CI runners. | - `--wheel-dir <dir>` points to a directory of pre‑downloaded wheels.<br>- If a required wheel is missing, the tool fails with a clear “wheel not found” error. |

### **E4 – Build Configuration & Customisation**  

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E4‑01** | As a **designer**, I want to specify an icon for the executable (`--icon <file.ico>`), so that the binary looks professional on Windows/macOS. | - Icon file is embedded and displayed in Explorer/Finder.<br>- Invalid icon path yields a warning but does not abort the build. |
| **E4‑02** | As a **developer**, I want to choose the target platform (`--target linux|windows|macos`) from a supported host, so that I can cross‑compile when possible. | - When the host OS matches the target, packaging proceeds normally.<br>- When cross‑compiling is unsupported, the tool prints a helpful “cross‑compile not available on this host” message. |
| **E4‑03** | As a **developer**, I want to enable optional compression (`--compress`) to reduce binary size, so that distribution bandwidth is lower. | - Binary size is reduced by at least 20 % on average for typical scripts.<br>- Decompression overhead at runtime is < 200 ms. |
| **E4‑04** | As a **developer**, I want to set a custom entry‑point (`--entry <module:function>`) for packages that expose a CLI, so that the executable runs the correct function. | - The generated binary invokes the specified function when executed.<br>- Invalid entry‑point strings cause a clear validation error before build starts. |

### **E5 – Distribution & Versioning**  

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E5‑01** | As a **release manager**, I want the binary filename to include the script name and version (`script‑v1.2.3‑linux`), so that artifacts are self‑describing. | - Version is taken from `--version` flag or from a `__version__` attribute if present.<br>- Filename pattern: `<name>-v<semver>-<os>-<arch>.exe?` |
| **E5‑02** | As a **user**, I want a SHA‑256 checksum file generated alongside the binary, so that I can verify integrity after download. | - A `<binary>.sha256` file is written containing `<hash>  <filename>` in standard format. |
| **E5‑03** | As a **devops engineer**, I want an optional `--publish <url>` flag that uploads the artifact to a simple HTTP index, so that teams can fetch the latest build automatically. | - On success, the tool prints the public URL of the uploaded binary.<br>- Failure to upload aborts the process with a non‑zero exit code. |
| **E5‑04** | As a **developer**, I want the tool to respect a `--output-dir <path>` argument, so that build artifacts are placed where I expect them. | - All generated files (binary, checksum, optional metadata) appear in the specified directory.<br>- Directory is created if it does not exist. |

### **E6 – Quality & Reliability**  

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E6‑01** | As a **QA engineer**, I want a comprehensive test suite (unit + integration) that runs on CI, so that regressions are caught early. | - `pytest` coverage ≥ 90 % for core modules.<br>- CI pipeline builds a sample script on Linux, Windows (via cross‑compile stub), and macOS (via emulation) and verifies execution. |
| **E6‑02** | As a **maintainer**, I want the project to enforce type‑checking (`mypy`) and linting (`ruff`), so that code quality stays high. | - CI fails if `mypy` reports any errors or if `ruff` warnings exceed a configurable threshold. |
| **E6‑03** | As a **user**, I want the binary to start within 1 second on a typical workstation, so that the tool feels snappy. | - Measured startup time ≤ 1 s on a machine with 4 CPU cores and 8 GB RAM (Linux). |
| **E6‑04** | As a **developer**, I want clear documentation (README, usage examples, FAQ) generated from the same source, so that the docs stay in sync with code. | - `mkdocs` site builds without warnings.<br>- `README` includes a “Quick Start” section that mirrors the CLI help output. |

---

## MVP Ordering (first release)

1. **E1‑01**, **E1‑02**, **E3‑01**, **E3‑02**, **E2‑01**, **E2‑02**, **E4‑01**, **E5‑01**, **E5‑02**, **E6‑01**, **E6‑02**  
   *Core packaging, basic CLI, dependency handling, simple customisation, versioned output, and test coverage.*

2. **E1‑03**, **E2‑03**, **E3‑04**, **E4‑02**, **E4‑03**, **E4‑04**, **E5‑03**, **E5‑04**  
   *Determinism, richer error messages, offline builds, cross‑compile support, compression, entry‑point overrides, publishing, output directory.*

3. **E6‑03**, **E6‑04**  
   *Performance benchmark, documentation generation.*

---

*All stories are written to be **shippable**: they describe a single, testable behavior with clear acceptance criteria, enabling incremental delivery and continuous validation.*

# TECH_SPEC.md  

## Project: script‑share – “Packager”  
**Goal**: Generate a single, self‑contained executable from an arbitrary Python script together with all of its runtime dependencies. The resulting binary can be distributed and run on target machines without requiring a pre‑installed Python interpreter or external libraries.

---  

### 1. Architecture Overview  

```
+-------------------+        +-------------------+        +-------------------+
|   CLI Interface   |  --->  |   Analyzer Engine |  --->  |   Bundler Engine  |
+-------------------+        +-------------------+        +-------------------+
                                 |                         |
                                 v                         v
                        +-------------------+    +-------------------+
                        | Dependency Graph  |    |  Bootstrapper    |
                        +-------------------+    +-------------------+
                                 |                         |
                                 +-----------+-------------+
                                             |
                                             v
                                    +-------------------+
                                    |   Standalone EXE  |
                                    +-------------------+
```

* **CLI Interface** – Parses user arguments, validates input, and drives the pipeline.  
* **Analyzer Engine** – Statically inspects the target script, builds a complete import‑dependency graph (including transitive imports, data files, native extensions).  
* **Bundler Engine** – Packages the interpreter, compiled byte‑code, native wheels, and resource files into a single archive; then prepends a custom bootstrapper.  
* **Bootstrapper** – Minimal C/Go stub (or frozen Python) that extracts the archive to a temporary location, sets up `sys.path`, and launches the entry‑point script.  

All components are pure‑Python except the bootstrapper, which is compiled once per target platform (Linux‑x86_64, macOS‑arm64, Windows‑x86_64).

---  

### 2. Core Components  

| Component | Responsibility | Key Modules / Files | Public API |
|-----------|----------------|---------------------|------------|
| **CLI** | Argument parsing, validation, orchestrates pipeline | `script_share/cli.py` | `main(argv: List[str]) -> int` |
| **Analyzer** | AST parsing, import resolution, detection of data files, native extensions | `script_share/analyzer.py` | `analyze(entry_path: Path) -> AnalysisResult` |
| **Bundler** | Collects interpreter binaries, wheels, creates zip‑app, invokes bootstrapper builder | `script_share/bundler.py` | `bundle(result: AnalysisResult, opts: BundleOptions) -> Path` |
| **Bootstrapper Builder** | Generates platform‑specific stub, embeds archive offset | `script_share/bootstrapper/` (C source + build script) | `build_stub(target: Platform) -> Path` |
| **Utilities** | Logging, hashing, temporary‑dir management | `script_share/utils/*.py` | – |

---  

### 3. Data Model  

```python
# script_share/models.py
from pathlib import Path
from typing import List, Set, NamedTuple, Literal

Platform = Literal["linux_x86_64", "macos_arm64", "windows_x86_64"]

class Dependency(NamedTuple):
    name: str                # e.g. "requests"
    version: str             # PEP‑440 version string
    wheel_path: Path | None  # Path to .whl if available
    is_builtin: bool         # stdlib modules

class Resource(NamedTuple):
    src: Path                # Original location on host
    dest: Path               # Relative path inside the bundle

class AnalysisResult(NamedTuple):
    entry_script: Path
    python_version: str
    dependencies: Set[Dependency]
    resources: Set[Resource]   # e.g. data files referenced via pkg_resources
    platform: Platform

class BundleOptions(NamedTuple):
    output_path: Path
    compress: bool = True
    upx_compress: bool = False   # optional binary compression
    strip_debug: bool = False
```

The **bundle archive** is a zip‑app (`.zip` with a `__main__.py` shim) that contains:

* `__bootstrap__/` – the extracted interpreter and stub files.  
* `site-packages/` – all wheels unpacked.  
* `app/` – the user script (`__main__.py`) and any bundled resources.  

The final executable layout:

```
<stub binary> | <4‑byte little‑endian archive offset> | <zip‑app>
```

---  

### 4. Key APIs / Interfaces  

#### 4.1 CLI  

```bash
script-share pack \
    --script path/to/app.py \
    --output dist/app.exe \
    --platform windows_x86_64 \
    [--compress] [--upx] [--strip]
```

* `--script` – required entry point.  
* `--output` – target executable path.  
* `--platform` – cross‑compile target (must match host for now).  
* Flags control optional post‑processing (UPX, stripping).

#### 4.2 Python Library  

```python
from script_share import pack

bundle_path = pack(
    entry_script=Path("my_app.py"),
    output=Path("dist/my_app"),
    platform="linux_x86_64",
    compress=True,
    upx_compress=False,
)
```

* Returns the absolute path to the generated executable.  

#### 4.3 Internal API (used by CI / tests)

```python
from script_share.analyzer import analyze
from script_share.bundler import bundle, BundleOptions

analysis = analyze(Path("my_app.py"))
options = BundleOptions(output_path=Path("dist/my_app"), compress=True)
exe_path = bundle(analysis, options)
```

---  

### 5. Technology Stack  

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Language** | Python ≥3.9 (runtime) | Modern syntax, typing, wide ecosystem |
| **Static Analysis** | `ast`, `importlib.metadata`, `modulefinder` | No external heavy dependencies |
| **Packaging** | `zipapp`, `wheel`, `pip` (internal API) | Leverages existing wheel format |
| **Bootstrapper** | C (compiled with `gcc`/`clang` on *nix, MSVC on Windows) | Small binary footprint, direct OS syscalls |
| **Compression** | `zstandard` (optional) + optional `UPX` | Faster decompression, optional size reduction |
| **Testing** | `pytest`, `tox` | Cross‑platform test matrix |
| **CI/CD** | GitHub Actions (Linux, macOS, Windows runners) | Automated build & validation |
| **Distribution** | PyPI package `script-share` + pre‑built stubs in `script_share/bootstrapper/bin/` | Easy install, versioned binaries |

---  

### 6. Dependencies  

| Dependency | Version | License |
|------------|---------|---------|
| `click` | ^8.1 | BSD‑3 |
| `tomli` | ^2.0 | MIT |
| `zstandard` | ^0.22 | BSD‑3 |
| `wheel` | ^0.42 | MIT |
| `setuptools` | ^70.0 | MIT |
| `cffi` (for stub building on Windows) | ^1.16 | MIT |
| `upx` (optional external tool) | ≥4.0 | GPL‑2 (optional) |

All dependencies are declared in `pyproject.toml` and installed in an isolated build environment.

---  

### 7. Deployment & Runtime  

1. **Build Stubs** – Executed once per platform during CI. Stubs are stored in `script_share/bootstrapper/bin/<platform>/stub`.  
2. **Package Release** – Publish to PyPI as `script-share`. Wheels contain the pre‑built stubs for the three supported platforms.  
3. **User Installation** – `pip install script-share`. Users run `script-share pack …`.  
4. **Execution Flow** (runtime):  
   * Stub binary starts → reads offset → extracts embedded zip to a secure temp dir (`%TMP%` / `/tmp`).  
   * Sets `PYTHONHOME` to the extracted interpreter, updates `sys.path` with bundled `site-packages`.  
   * Executes `app/__main__.py`.  
   * On exit, cleans up temporary directory (unless `--no-cleanup` flag is added in future).  

---  

### 8. Security & Hardening  

* **Signature verification** – The stub verifies a SHA‑256 hash of the embedded archive before extraction (hash stored in the stub header).  
* **Sandboxing** – Execution occurs in a temporary directory with restrictive permissions (`chmod 700`).  
* **No network access** – The bundled interpreter is launched with `-B` (no `sitecustomize`) to avoid accidental import of malicious site‑packages.  

---  

### 9. Testing Strategy  

| Test Type | Scope | Tooling |
|-----------|-------|---------|
| Unit | Analyzer import resolution, bundler file inclusion | `pytest` + `pytest-mock` |
| Integration | End‑to‑end pack → run on each platform | Docker containers (linux), macOS runner, Windows runner |
| Performance | Binary size, startup latency | `time`, `hyperfine` |
| Security | Archive tampering detection | Fuzzing with `afl` on stub header parsing |

Coverage target: **≥90 %** for core modules.

---  

### 10. Future Enhancements (Roadmap)  

| Milestone | Feature | Impact |
|-----------|---------|--------|
| v0.2 | Cross‑compilation (build Windows exe from Linux) | Broader CI capability |
| v0.3 | Plug‑in system for custom resource collectors (e.g., PyQt assets) | Extensibility |
| v0.4 | GUI front‑end (Electron/tauri) for non‑technical users | Market reach |
| v0.5 | Remote cache of pre‑built interpreter layers (reduces bundle size) | Size reduction |

---  

### 11. Glossary  

* **Stub** – Small native binary that bootstraps the bundled Python environment.  
* **Archive offset** – 4‑byte little‑endian integer placed after the stub indicating where the zip‑app starts.  
* **UPX** – Ultimate Packer for Executables, optional post‑process compression.  

---  

### 12. References  

* Python `zipapp` documentation – https://docs.python.org/3/library/zipapp.html  
* Wheel spec – https://www.python.org/dev/peps/pep-0427/  
* vLLM (in‑house inference engine) – not directly used but available in the company knowledge base for future AI‑assisted code analysis.  

---  

*Prepared by the senior product/engineering lead, 2026‑06‑25.*

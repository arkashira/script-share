# Product Requirements Document (PRD)

## Project: **script‑share**

**Owner:** Senior Product/Engineering Lead  
**Target Release:** Q4 2026 (Beta)  
**Repository:** `script-share` (Packager – generate a standalone executable from a Python script and its dependencies)

---

### 1. Problem Statement  

Python developers frequently need to distribute small utilities or prototypes to non‑technical users. Current options (e.g., PyInstaller, cx_Freeze, Docker) require manual configuration, platform‑specific builds, or a runtime environment, creating friction and limiting adoption.  

**Resulting pain points**

| Pain Point | Who Experiences It | Impact |
|------------|-------------------|--------|
| **Complex build steps** – multiple commands, hidden dependencies, platform quirks. | Python developers, data scientists, internal tooling teams | Delays release, increases support tickets. |
| **Non‑technical recipients cannot run scripts** – must install Python, manage virtualenvs. | End‑users (product managers, analysts, customers) | Low adoption, reliance on internal devs for simple tasks. |
| **Version drift** – shared scripts quickly become incompatible with target machines. | All stakeholders | Bugs, security exposure, lost trust. |

A streamlined, one‑click solution that turns any Python script (with its imports) into a **single, portable executable** will eliminate these frictions and open a new distribution channel for internal tools, SaaS extensions, and community‑driven scripts.

---

### 2. Target Users  

| Segment | Description | Primary Needs |
|---------|-------------|---------------|
| **Internal developers** | Engineers building internal utilities for ops, data, or product teams. | Fast, reproducible packaging; minimal CI/CD changes. |
| **Product managers / analysts** | Non‑technical users who need to run simple scripts on their laptops. | Click‑to‑run executables, no setup required. |
| **Open‑source community** | Contributors sharing reusable scripts on GitHub, forums, or internal marketplaces. | Easy packaging, clear versioning, cross‑platform binaries. |
| **Enterprise IT** | Teams distributing vetted tools across heterogeneous workstations. | Secure, signed executables; auditability. |

---

### 3. Goals & Success Metrics  

| Goal | Metric | Target (6 mo) |
|------|--------|---------------|
| **Reduce packaging friction** | Avg. time from script commit to executable generation (CI) | ≤ 5 min |
| **Increase adoption** | Number of unique executables generated per month (internal + external) | 1,200 |
| **Cross‑platform support** | Successful builds on Windows, macOS, Linux (Ubuntu 22.04) | 100 % |
| **Reliability** | Build success rate (CI pipelines) | ≥ 98 % |
| **Security** | Executables signed with company key & pass verification | 100 % |
| **User satisfaction** | NPS from internal beta participants | ≥ +45 |

---

### 4. Scope  

#### In‑Scope (Must‑Have)

1. **CLI Packager** – `script-share pack <script.py> [--output <file>]`  
   - Detects imports, resolves dependencies via `pip`/`requirements.txt`.  
   - Bundles Python interpreter (embedded) and compiled bytecode into a single executable.  
   - Supports **Windows (exe)**, **macOS (app)**, **Linux (elf)**.

2. **Dependency Isolation**  
   - Uses virtual environment isolation to avoid host contamination.  
   - Option `--requirements <path>` to specify exact versions.

3. **Cross‑Platform Build Engine**  
   - Leverages **vLLM** for fast dependency resolution caching.  
   - Utilises **SGLang** for structured generation of build manifests.

4. **CI/CD Integration**  
   - GitHub Action `script-share/build` that runs on push/tag and uploads artifact to GitHub Releases.  
   - Configurable via `script-share.yml`.

5. **Executable Signing**  
   - Automatic code signing on Windows (Authenticode) and macOS (Developer ID).  
   - Configurable signing key via environment variables.

6. **Documentation & Templates**  
   - README with quick‑start, troubleshooting, and best‑practice guide.  
   - Example repository (`script-share/example`) with a sample script and CI workflow.

#### Out‑of‑Scope (Will Not Be Delivered in This Release)

| Item | Reason |
|------|--------|
| **GUI Builder** | Focus on CLI for rapid iteration; GUI can be added later. |
| **Runtime Update Mechanism** | Requires separate versioning service; postponed to v2. |
| **Docker / Container Output** | Not a primary user need for standalone executables. |
| **Multi‑language support** (e.g., R, Julia) | Scope limited to Python for now. |
| **Enterprise license management** | Handled by existing internal tooling. |

---

### 5. Key Features (Prioritized)

| Priority | Feature | Description | Acceptance Criteria |
|----------|---------|-------------|----------------------|
| **P1** | **One‑Command Packager** | `script-share pack` produces a single binary. | Binary runs on target OS without installing Python; `--help` displays usage. |
| **P1** | **Automatic Dependency Detection** | Parses `import` statements, resolves from PyPI. | All imported packages are bundled; missing packages raise clear error. |
| **P1** | **Cross‑Platform Build** | Single source repo builds for Windows/macOS/Linux. | CI builds succeed on all three OS runners. |
| **P2** | **Configurable Build Manifest** | `script-share.yml` to pin Python version, extra files, post‑install hooks. | Build respects manifest entries; fails with informative message on invalid config. |
| **P2** | **Code Signing** | Sign executables with provided key. | Signed binaries pass OS verification tools (`sigcheck`, `codesign`). |
| **P3** | **Versioned Release Artifacts** | Auto‑publish to GitHub Releases with semver tag. | Tag `vX.Y.Z` creates release containing binaries for all platforms. |
| **P3** | **Telemetry (opt‑in)** | Collect anonymous success/failure metrics. | Dashboard shows build success rate; respects privacy flag. |
| **P4** | **Plugin System** | Allow custom pre‑/post‑build steps via Python plugins. | Sample plugin executes during build and modifies output. |

---

### 6. User Journeys  

1. **Developer** pushes a new script to `main`.  
   - CI triggers `script-share/build`.  
   - Build resolves deps, creates `mytool-windows.exe`, `mytool-macos.app`, `mytool-linux`.  
   - Artifacts are signed and uploaded to GitHub Release `v1.2.0`.  

2. **Product Manager** downloads `mytool-windows.exe` from the release page, double‑clicks, and the tool runs instantly, no Python install needed.  

3. **IT Admin** verifies the signature using internal policy tools, confirms the binary matches the approved version, and distributes it via SCCM.

---

### 7. Technical Requirements  

| Area | Requirement |
|------|-------------|
| **Language** | Python 3.11+ (runtime embedded) |
| **Build Tooling** | vLLM for dependency graph caching; SGLang for manifest generation |
| **Packaging** | Use `zipapp` + bundled interpreter or `pyinstaller` as fallback; ensure deterministic builds |
| **CI** | GitHub Actions matrix (ubuntu‑latest, windows‑latest, macos‑latest) |
| **Signing** | Windows: `signtool`; macOS: `codesign` – keys stored in GitHub Secrets |
| **Telemetry** | Optional `POST` to internal endpoint; respect `SCRIPT_SHARE_TELEMETRY=0` |
| **License** | MIT (compatible with bundled dependencies) |
| **Security** | Run builds in isolated containers; verify no network access beyond PyPI; scan final binary with Trivy. |

---

### 8. Milestones & Timeline  

| Milestone | Deliverable | Owner | Due |
|-----------|-------------|-------|-----|
| **M1 – Foundations** | CLI skeleton, dependency resolver, basic packaging for Linux | Lead Engineer | Week 2 |
| **M2 – Cross‑Platform** | Windows & macOS binary generation, CI matrix | Platform Engineer | Week 5 |
| **M3 – Signing & Release** | Automated code signing, GitHub Release workflow | DevOps Lead | Week 7 |
| **M4 – Documentation & Templates** | README, example repo, user guide | Technical Writer | Week 8 |
| **M5 – Beta Launch** | Internal beta with 5 teams, collect feedback | PM | Week 10 |
| **M6 – GA Release** | Public GitHub release, telemetry dashboard | PM/Eng Lead | Week 12 |

---

### 9. Risks & Mitigations  

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Dependency bloat** – large binaries may exceed size limits. | Users may reject large downloads. | Enable optional `--strip` flag; use UPX compression; allow exclusion of optional packages. |
| **Platform-specific bugs** (e.g., macOS notarization). | Build failures on certain OS versions. | Early testing on all three OS runners; maintain a “known‑good” Python interpreter build. |
| **Signing key leakage** | Security breach, loss of trust. | Store keys in GitHub Secrets, rotate quarterly, enforce MFA. |
| **Telemetry privacy concerns** | Legal/compliance issues. | Opt‑in only; clear privacy notice; no PII collected. |
| **PyPI outage** during build | Build failures. | Cache resolved wheels in S3 bucket; fallback to local mirror. |

---

### 10. Approval  

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner |  |  |  |
| Engineering Lead |  |  |  |
| UX / Documentation Lead |  |  |  |
| Security Officer |  |  |  |

--- 

*End of Document*

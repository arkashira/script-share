# ROADMAP.md

## 📅 Overview
**Project:** `script-share` – a lightweight packager that turns a Python script (and its runtime dependencies) into a single, portable executable.  
**Goal:** Enable developers to share runnable Python tools without requiring recipients to install Python or manage dependencies.

---

## 🚀 MVP (Minimum Viable Product) – **Launch‑Ready**

| Milestone | Description | Acceptance Criteria | MVP‑Critical |
|-----------|-------------|---------------------|--------------|
| **M1 – Core CLI Packager** | `script-share pack <script.py> [--output <file>]` | - Accepts a Python entry‑point file.<br>- Resolves **runtime imports** (standard lib + `requirements.txt` or `pyproject.toml`).<br>- Bundles a minimal Python interpreter (embedded CPython) into a single executable.<br>- Works on **Linux x86_64** (primary target). | ✅ |
| **M2 – Dependency Isolation** | Use **virtual‑environment style isolation** to avoid host‑system packages. | - Packages only the declared dependencies.<br>- Verifies that the generated exe runs on a clean container (no Python installed). | ✅ |
| **M3 – Basic Configuration Flags** | `--onefile`, `--icon <path>`, `--entrypoint <func>` | - `--onefile` produces a single binary (default).<br>- `--icon` embeds a Windows `.ico` (optional, ignored on other OS).<br>- `--entrypoint` allows specifying a callable other than `if __name__ == "__main__"`. | ✅ |
| **M4 – Cross‑Platform Build Scripts** | Simple Docker‑based build images for **Linux**, **macOS**, **Windows** (via `wine`/`cross‑compile`). | - `script-share build --platform linux|mac|win` produces a runnable binary for the target OS.<br>- Documentation includes usage examples. | ✅ |
| **M5 – Automated Tests & CI** | GitHub Actions pipeline validates packaging on all three platforms. | - Tests cover successful packaging, execution, and missing‑dependency errors.<br>- CI badge displayed in README. | ✅ |
| **M6 – Documentation** | Clear README, quick‑start guide, and CLI help (`script-share --help`). | - Users can go from “zero” to “executable” in ≤5 minutes.<br>- FAQ section for common pitfalls (e.g., native extensions). | ✅ |

**MVP Completion Target:** **8 weeks** from kickoff.

---

## 🌟 Version 1 – Feature Expansion

| Theme | Target Release | Key Features |
|-------|----------------|--------------|
| **V1‑A: User Experience** | **Week 9‑14** | - **Interactive wizard** (`script-share init`) that creates a minimal project scaffold (setup.cfg, requirements.txt).<br>- **Progress bar** and verbose logging.<br>- **Dry‑run mode** (`--dry-run`) to preview packaged files. |
| **V1‑B: Enhanced Compatibility** | **Week 15‑20** | - Support for **Python 3.9‑3.12** (multiple interpreter bundles).<br>- Proper handling of **native wheels** (e.g., `numpy`, `pandas`).<br>- **macOS notarization** option for distribution. |
| **V1‑C: Distribution & Updates** | **Week 21‑26** | - **Self‑updating executable** (checks a signed manifest on launch).<br>- Ability to **embed a small HTTP server** for auto‑download of newer releases.<br>- **Checksum verification** of bundled files. |
| **V1‑D: Security Hardenings** | **Week 27‑30** | - **Code signing** support for Windows (`signtool`) and macOS (`codesign`).<br>- Optional **runtime sandbox** (via `seccomp` on Linux).<br- **License compliance** scan (detect GPL‑linked libs). |

---

## 🚀 Version 2 – Ecosystem & Scalability

| Theme | Target Release | Key Features |
|-------|----------------|--------------|
| **V2‑A: Plugin Architecture** | **Week 31‑38** | - Public **plugin SDK** to add custom pre‑/post‑packaging steps (e.g., minify assets, embed config).<br>- Marketplace‑style **plugin registry** (GitHub‑based). |
| **V2‑B: Cloud Build Service** | **Week 39‑46** | - Hosted **build API** (`POST /build`) that returns a download URL for the exe.<br>- **Authentication** (API keys, OAuth).<br>- **Usage metering** for billing (aligned with Axentx revenue‑validation). |
| **V2‑C: Collaboration & Sharing** | **Week 47‑52** | - **Web UI** to upload scripts, generate shareable links, and view build logs.<br>- **Versioning** of packaged artifacts.<br>- Integration with **GitHub Actions** (auto‑package on release). |
| **V2‑D: Enterprise Controls** | **Week 53‑60** | - **Policy engine** to enforce allowed dependencies (e.g., disallow GPL).<br>- **Audit logs** for compliance teams.<br>- **On‑premise deployment** option for isolated networks. |

---

## 📌 Milestone Tracking & Ownership

| Milestone | Owner | Status (Start → End) |
|-----------|-------|----------------------|
| M1‑M6 (MVP) | **Core Team** (CLI, Build, CI) | Week 1 → Week 8 |
| V1‑A | **UX Lead** | Week 9 → Week 14 |
| V1‑B | **Platform Engineer** | Week 15 → Week 20 |
| V1‑C | **Ops / Security** | Week 21 → Week 26 |
| V1‑D | **Security Lead** | Week 27 → Week 30 |
| V2‑A | **Plugin Lead** | Week 31 → Week 38 |
| V2‑B | **Cloud Engineer** | Week 39 → Week 46 |
| V2‑C | **Product Designer** | Week 47 → Week 52 |
| V2‑D | **Enterprise PM** | Week 53 → Week 60 |

---

## 📈 Success Metrics

| Metric | Target (by end of MVP) | Target (by end of V2) |
|--------|------------------------|-----------------------|
| **Packaging Success Rate** | ≥ 95 % on clean CI containers | ≥ 98 % across all supported OS |
| **CLI Adoption** | 200+ unique GitHub stars | 1 k+ stars, 500+ daily downloads |
| **Time‑to‑Executable** | ≤ 30 seconds for typical script (<10 deps) | ≤ 20 seconds with cloud build |
| **Customer‑Validated Pain** | ≥ 30 paid pilot users (via Axentx validation) | ≥ 200 paying customers, churn < 5 % |
| **Revenue** | $5k ARR from early adopters | $150k ARR by end of Year 2 |

---

## 📚 References

- **Chain Playbook (2026‑06‑21)** – ensures each milestone is “Go/No‑Go” gated.
- **C. Frameworks** – we will leverage `vLLM` for any future AI‑assisted dependency resolution and `SGLang` for structured CLI generation.
- **Existing Portfolio** – no overlap with `iceoryx2` (IPC library) – `script-share` expands the toolchain offering.

--- 

*Prepared by the Senior Product/Engineering Lead – Axentx OS*

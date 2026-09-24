# NOTES: fulltech-platform-skills

## Current work: linux-sanitizer (branch `feat/linux-sanitizer`, uncommitted)

Decision (2026-09-24): a single `linux-sanitizer` plugin with WSL detected as an environment mode. No separate `wsl-sanitizer`. Host-side WSL tasks (vhdx, `.wslconfig`) go into `windows-sanitizer`.
v1 scope: Debian/Ubuntu (apt). Other distros: generic checks only.

| Wave | Status | Evidence |
|---|---|---|
| 1. `triage.sh` | done | shellcheck clean; host (vm/kvm) ~57s; container ok; WSL branch **simulated** (forced detection + fake wsl.conf/.wslconfig) |
| 2a. `remediate.sh` | done | host dry-run: hashes/du unchanged; container `--apply --yes` ok and idempotent; non-root refused; 3 wsl.conf cases + generateHosts refusal ok |
| 2b. WSL in windows-sanitizer | code done, **not tested on Windows** | pwsh parser: 0 errors; prefix regex and JSON depth 4 tested in pwsh on Linux |
| 3. report/SKILL/plugin/marketplace/READMEs | done | `claude plugin validate .` passes; install in isolated CLAUDE_CONFIG_DIR ok |

## Decisions made during implementation
- Telemetry is **disabled**, not purged: purging popularity-contest/apport removes ubuntu-standard/ubuntu-desktop, and a later autoremove would remove unrelated packages.
- WSL compaction uses `Optimize-VHD` (Hyper-V) or `diskpart compact vdisk`. `wsl --manage --set-sparse` was dropped because sparse VHD support was disabled in some WSL 2.x releases over corruption risk.
- `docker system df` capped at 30s (took 177s on the VILI host).
- New environment type `container` (needed for tests; systemd-detect-virt -c or /.dockerenv).

## Pending
- [ ] Real test in WSL2: `triage.sh`, `remediate.sh --wsl-windows-path`, `remediate.ps1 -CompactWslDisks` (record GB before/after here).
- [ ] Commits: (1) feat linux-sanitizer + WSL in windows-sanitizer; (2) fix `skills: ["./"]` in android/ios/windows plugin.json (separate so it can be reverted).
- [ ] After merge: `claude plugin marketplace update fulltech-platform-skills` + install + invoke the skill in a fresh session.

## Pre-existing issues (not fixed here)
- `windows_triage.json` / `windows_report.html` committed (root and plugin): run outputs, candidates for `.gitignore`.
- `category` in android/ios/windows plugin.json: validator warning (unused field).
- Root README.pt-BR.md / README.es.md don't list windows-sanitizer (nor ios in the table).
- `plugins/ios-sanitizer/relatorio_forense_iphone11.html`: a real report committed (check for personal data).

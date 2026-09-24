# NOTES: fulltech-platform-skills

## Current work: linux-sanitizer (branch `feat/linux-sanitizer`, uncommitted)

Decision (2026-09-24): a single `linux-sanitizer` plugin with WSL detected as an environment mode. No separate `wsl-sanitizer`. Host-side WSL tasks (vhdx, `.wslconfig`) go into `windows-sanitizer`.
v1 scope: Debian/Ubuntu (apt). Other distros: generic checks only.

| Wave | Status | Evidence |
|---|---|---|
| 1. `triage.sh` | done | shellcheck clean; host (vm/kvm) ~57s; container ok; WSL branch **simulated** (forced detection + fake wsl.conf/.wslconfig) |
| 2a. `remediate.sh` | done | host dry-run: hashes/du unchanged; container `--apply --yes` ok and idempotent; non-root refused; 3 wsl.conf cases + generateHosts refusal ok |
| 2b. WSL in windows-sanitizer | done | Tested on Windows 11 24H2 with WSL 2.3.24.0. Sparse VHDX handling added with fstrim. |
| 3. report/SKILL/plugin/marketplace/READMEs | done | `claude plugin validate .` passes; reports generated on Windows and Linux. |

## Decisions made during implementation
- Telemetry is **disabled**, not purged: purging popularity-contest/apport removes ubuntu-standard/ubuntu-desktop, and a later autoremove would remove unrelated packages.
- WSL compaction: `Optimize-VHD` / `diskpart compact vdisk` are used for standard VHDX. If the VHDX has the `SparseFile` attribute (via `sparseVhd=true`), Windows disk attachment rejects compacting with a virtual disk limitation error; for sparse disks, `fstrim -v /` inside WSL is executed to reclaim unallocated space dynamically.
- `docker system df` capped at 30s (took 177s on the VILI host).
- New environment type `container` (needed for tests; systemd-detect-virt -c or /.dockerenv).

## Completed Tasks
- [x] Real test in WSL2: `triage.sh` (6s), `remediate.sh --apply` (cleaned 440MB journal, 120MB apt cache, disabled apport/motd-news, set appendWindowsPath=false reducing PATH from 69 to 0 entries).
- [x] Tested `remediate.ps1 -CompactWslDisks` with native sparse VHDX detection and internal fstrim.
- [x] Consolidated work directly to `main` and pushed to GitHub.

## Pre-existing issues (not fixed here)
- `windows_triage.json` / `windows_report.html` committed (root and plugin): run outputs, candidates for `.gitignore`.
- `category` in android/ios/windows plugin.json: validator warning (unused field).
- Root README.pt-BR.md / README.es.md don't list windows-sanitizer (nor ios in the table).
- `plugins/ios-sanitizer/relatorio_forense_iphone11.html`: a real report committed (check for personal data).

# Linux Sanitizer (Linux + WSL)

<p align="center">
  <strong>🌐 Multi-Language Documentation</strong><br>
  <a href="README.md"><b>English</b></a> •
  <a href="README.pt-BR.md"><b>Português (Brasil)</b></a> •
  <a href="README.es.md"><b>Español</b></a>
</p>

An agent skill for read-only triage and dry-run-first cleanup of Ubuntu/Debian systems, including distros running under WSL.

---

## 🎯 Highlights

- **Automatic environment detection:** bare metal, VM, container, WSL1 and WSL2; checks adapt to each.
- **Disk-space recovery:** apt cache, systemd journal, old snap revisions; Docker and `~/.cache` are reported, never deleted.
- **Telemetry deactivation:** apport, whoopsie, popularity-contest, ubuntu-report, motd-news (disabled, not purged, to avoid metapackage removal).
- **WSL aware:** reads `wsl.conf`, flags Windows PATH pollution, refuses to edit an auto-generated `/etc/hosts`.
- **Safe by default:** remediation is a dry-run unless `--apply` is passed with sudo.

---

## 📂 Structure

- [`SKILL.md`](./SKILL.md) — Agent instructions and workflow.
- [`scripts/triage.sh`](./scripts/triage.sh) — Read-only triage, writes `linux_triage.json`.
- [`scripts/remediate.sh`](./scripts/remediate.sh) — Remediation (dry-run by default).
- [`scripts/generate_report.py`](./scripts/generate_report.py) — HTML report (fulltech.app design system).

> The Windows side of WSL (`ext4.vhdx` compaction, `.wslconfig`) lives in [`windows-sanitizer`](../windows-sanitizer/) (`-CompactWslDisks`).

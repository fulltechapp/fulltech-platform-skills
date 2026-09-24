# Android Sanitizer & Adware Remediation

<p align="center">
  <strong>🌐 Multi-Language Documentation</strong><br>
  <a href="README.md"><b>English</b></a> •
  <a href="README.pt-BR.md"><b>Português (Brasil)</b></a> •
  <a href="README.es.md"><b>Español</b></a>
</p>

An intelligent, multi-harness agent skill for diagnosing, sanitizing, and protecting Android devices connected via ADB.

---

## 🎯 Highlights

- **Elderly Care & Casual Mode:** Preserves user games (Candy Crush, Mahjong, Solitaire), banking, medical, and personal apps while eliminating ads via Private DNS sinkhole.
- **Forensic Window Detection:** Catches intrusive ads live on screen using `dumpsys window`.
- **Overlay & Permission Audit:** Identifies apps abusing `SYSTEM_ALERT_WINDOW` and Accessibility services.
- **OEM Adware Removal:** Curated lists for Xiaomi (HyperOS/MIUI), Samsung (One UI), Motorola, and Transsion.
- **Private DNS Sinkhole:** Automates AdGuard DNS (`dns.adguard-dns.com`) setup to block video ads and trackers across all apps.

---

## 📂 Structure

- [`SKILL.md`](./SKILL.md) — Main instructions and workflow for AI agents.
- [`scripts/triage.sh`](./scripts/triage.sh) — Bash automation helper (Linux/WSL/macOS).
- [`scripts/triage.ps1`](./scripts/triage.ps1) — PowerShell automation helper (Windows).
- [`references/oem_catalog.json`](./references/oem_catalog.json) — Database of OEM ad engines and bloatware packages.

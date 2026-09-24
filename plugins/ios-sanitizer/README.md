# iOS Sanitizer & Performance Diagnostics

<p align="center">
  <strong>🌐 Multi-Language Documentation</strong><br>
  <a href="README.md"><b>English</b></a> •
  <a href="README.pt-BR.md"><b>Português (Brasil)</b></a> •
  <a href="README.es.md"><b>Español</b></a>
</p>

An autonomous, multi-harness agent skill for diagnosing, sanitizing, and optimizing Apple iOS devices (iPhone, iPad) connected via USB or Wi-Fi Lockdown without Jailbreak.

---

## 🎯 Highlights

- **BMS Hardware Battery Forensics:** Reads raw cycle counts, factory design mAh, actual nominal charge capacity, and battery temperature directly from the Battery Management System registers via IORegistry (`AppleSmartIOBattery`).
- **CPU Performance Throttling Diagnosis:** Identifies when iOS Dynamic Performance Management has downclocked the A-series SoC due to cell wear (>1000 cycles or <80% health).
- **Kernel Panic & Memory Forensics:** Audits `/Panics` and diagnostic reports to verify motherboard/hardware health and detect memory-exhausting `JetsamEvent` crashes.
- **Application & Migration Inventory:** Detects and uninstalls residual migration apps (such as `CopyMyData`) and predatory subscription traps.
- **Malicious Profile Auditing:** Inspects and removes rogue MDM profiles, proxy configurations, and corporate certificates.
- **Native Encrypted DNS Ad-Sinkhole:** Generates and serves Apple Configuration Profiles (`.mobileconfig`) with DNS-over-HTTPS (DoH) to eliminate in-app and browser ads without VPN apps or battery drain.

---

## 📂 Structure

- [`SKILL.md`](./SKILL.md) — Main instructions and 5-step triage workflow for AI agents.
- [`scripts/triage.ps1`](./scripts/triage.ps1) — PowerShell autonomous diagnostic runner.
- [`scripts/triage_helper.py`](./scripts/triage_helper.py) — Async Python engine leveraging `pymobiledevice3` v11+.
- [`scripts/serve_profile.py`](./scripts/serve_profile.py) — Local HTTP server to deploy `.mobileconfig` profiles over Safari.
- [`profiles/adguard_dns.mobileconfig`](./profiles/adguard_dns.mobileconfig) — Encrypted DNS profile payload.
- [`references/ios_bundle_catalog.json`](./references/ios_bundle_catalog.json) — Catalog of predatory cleaner apps and ad networks.

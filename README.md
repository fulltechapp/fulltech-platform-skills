# Fulltech Platform Skills

<p align="center">
  <strong>🌐 Multi-Language Documentation</strong><br>
  <a href="README.md"><b>English</b></a> •
  <a href="README.pt-BR.md"><b>Português (Brasil)</b></a> •
  <a href="README.es.md"><b>Español</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Architecture-Multi--Harness-blue?style=for-the-badge&logo=anthropic" alt="Multi-Harness" />
  <img src="https://img.shields.io/badge/Claude%20Code-Compatible-8A2BE2?style=for-the-badge" alt="Claude Code" />
  <img src="https://img.shields.io/badge/Google%20Antigravity-Compatible-4285F4?style=for-the-badge&logo=google" alt="Google Antigravity" />
  <img src="https://img.shields.io/badge/skills.sh-Ecosystem-green?style=for-the-badge" alt="Skills.sh" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge" alt="License" />
</p>

---

> **Autonomous Multi-Harness Agent Skills, DevOps Engineering & Device Forensics Marketplace for Fulltech.**

This repository hosts production-ready, modular skills designed to run seamlessly across modern agentic coding harnesses: **Claude Code**, **Google Antigravity**, **Cursor**, **OpenAI Codex**, and **Orca**.

---

## 🌟 Spotlight Skill: `android-sanitizer`

> *"Why did Grandma's phone with 100% battery look completely dead until plugged into USB?"*

Most Android debloaters are static lists of package names. **`android-sanitizer`** is an **autonomous forensic triage agent** that connects via ADB, investigates system tombstones in real-time, diagnoses hardware-level driver crashes, and rehabilitates devices.

### 🔬 Real-World Case Study: The "Sleep of Death" (SOD) Adware Deadlock

During testing on a Snapdragon 660 device (Redmi Note 7), the phone exhibited classic **Sleep of Death (SOD)**:
- Battery was at **100% (4.39 V)**, yet the Power button could not wake the screen.
- Plugging in a USB cable generated a 5V PMIC interrupt that forced the display awake.

`android-sanitizer` queried low-level system tombstones (`dumpsys dropbox`) and unmasked the culprit:

```text
Timestamp: 2026-09-06 21:38:38-0300
Process: >>> /system/vendor/bin/mm-pp-dpps <<<
Signal: 6 (SIGABRT)
Abort message: 'Attempted to retrieve value from failed HIDL call: Status(EX_TRANSACTION_FAILED): DEAD_OBJECT'
```

**The Forensic Chain:**
1. At `21:03` to `21:35`, a cascade loop of free games with aggressive video interstitials was installed.
2. At `21:38`, when the screen turned off, hardware-accelerated video buffers (`SurfaceView`) collided with Xiaomi's Wallpaper Carousel (`fashiongallery`) attempting to project lockscreen ads.
3. Qualcomm's Display Post-Processing service (`mm-pp-dpps`) crashed into a `DEAD_OBJECT` deadlock.
4. **Remediation:** Purging the lockscreen pushers and video ad loop permanently solved the SOD, while freeing **~300 MB of RAM** and measuring a **98% battery health retention (3,923 mAh / 4,000 mAh)**!

---

## 📊 Comparison: Static Debloaters vs. `android-sanitizer`

| Capability | Traditional Debloaters (UAD, Canta) | `android-sanitizer` (Agent Skill) |
| :--- | :---: | :---: |
| **Conversational Triage** | ❌ No | ✅ **Autonomous AI Agent** |
| **Sleep-of-Death (SOD) Detection** | ❌ No | ✅ **Inspects tombstones & `mm-pp-dpps`** |
| **Cascade Loop ("Blue Dot") Audit** | ❌ No | ✅ **Clusters same-day ad install chains** |
| **Interactive User Questionnaire** | ❌ No | ✅ **Guided choices via `ask_question`** |
| **Elderly Care (Protect Games & Banks)**| ❌ Risk of breaking | ✅ **Preserves games, neuters ads** |
| **Hardware & Battery Wear Analysis** | ❌ No | ✅ **Learned mAh vs. Design capacity** |
| **Private DNS Ad-Sinkhole Automation**| ❌ Manual | ✅ **Automated Intent launcher** |
| **Multi-Harness Architecture** | ❌ Standalone GUI only | ✅ **Claude Code, Antigravity, Codex, Cursor** |

---

## 📦 Directory of Skills

| Skill | Category | Description | Supported Harnesses |
| :--- | :--- | :--- | :--- |
| [`android-sanitizer`](./plugins/android-sanitizer/) | Mobile Forensics / Optimization | Autonomous Android triage, adware remediation, SOD diagnosis, OEM bloatware removal (Xiaomi, Samsung, Motorola, Transsion), and Private DNS ad-sinkhole automation. | Claude Code, Antigravity, Cursor, Codex, Orca |
| [`ios-sanitizer`](./plugins/ios-sanitizer/) | Mobile Forensics / Optimization | Autonomous iOS triage, BMS health checks, malicious profile purging, and AdGuard DNS ad-sinkhole automation. | Claude Code, Antigravity, Cursor, Codex, Orca |
| [`windows-sanitizer`](./plugins/windows-sanitizer/) | OS Forensics / Optimization | Autonomous Windows PC triage, telemetry deactivation, UWP bloatware removal, and OS-level network sinkhole tracking blocking. | Claude Code, Antigravity, Cursor, Codex, Orca |

---

## 🚀 Installation & Usage

### 1. In Claude Code (via Marketplace)
Register this marketplace repository in Claude Code:
```bash
/plugin marketplace add fulltechapp/fulltech-platform-skills
```
Install the desired plugin:
```bash
/plugin install android-sanitizer
/plugin install ios-sanitizer
/plugin install windows-sanitizer
```

### 2. In Google Antigravity / Agentic Environments
Clone or copy the skill directory into your user or project agents directory:
```bash
# Global user level (available across all workspaces)
cp -r plugins/android-sanitizer ~/.agents/skills/
cp -r plugins/ios-sanitizer ~/.agents/skills/
cp -r plugins/windows-sanitizer ~/.agents/skills/
```

### 3. Via Open Skills CLI (`skills.sh`)
```bash
npx skills add fulltechapp/fulltech-platform-skills@android-sanitizer
npx skills add fulltechapp/fulltech-platform-skills@ios-sanitizer
npx skills add fulltechapp/fulltech-platform-skills@windows-sanitizer
```

---

## 🛠️ Repository Architecture

This repository adopts a **hybrid multi-harness standard**:

```text
fulltech-platform-skills/
├── .claude-plugin/
│   └── marketplace.json            # Claude Code / Claude Hub catalog index
├── plugins/
│   ├── android-sanitizer/          # Autonomous Android triage & forensics
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json         # Claude plugin descriptor
│   │   ├── SKILL.md                # Universal multi-harness agent instructions
│   │   ├── scripts/
│   │   │   ├── triage.sh           # POSIX bash helper (--health, --sod, --watch)
│   │   │   └── triage.ps1          # Windows PowerShell helper (-HealthCheck, -AuditSOD)
│   │   └── references/
│   │       └── oem_catalog.json    # Vendor ad engines & bloatware database
│   └── ios-sanitizer/              # Autonomous iOS triage & performance forensics
│       ├── .claude-plugin/
│       │   └── plugin.json         # Claude plugin descriptor
│       ├── SKILL.md                # Universal multi-harness agent instructions
│       ├── scripts/
│       │   ├── triage.ps1          # Autonomous PowerShell triage runner
│       │   ├── triage_helper.py    # Async BMS hardware & lockdown extractor
│       │   └── serve_profile.py    # Local profile server for 1-click DoH setup
│       ├── profiles/
│       │   └── adguard_dns.mobileconfig # Native Apple DoH encrypted DNS payload
│       └── references/
│           └── ios_bundle_catalog.json # Known predatory cleaner apps & ad networks
│   ├── windows-sanitizer/          # Autonomous Windows OS triage & debloater
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json         # Claude plugin descriptor
│   │   ├── SKILL.md                # Universal multi-harness agent instructions
│   │   ├── scripts/
│   │   │   ├── triage.ps1          # Windows health & telemetry audit script
│   │   │   ├── remediate.ps1       # Admin sinkhole & debloat remediation
│   │   │   └── generate_report.ps1 # Executive HTML Report engine
├── README.md                       # English documentation
├── README.pt-BR.md                 # Brazilian Portuguese documentation
└── README.es.md                    # Spanish documentation
```

---

## 🤝 Contributing

1. Create a new skill directory under `plugins/<skill-name>`.
2. Follow the standard `SKILL.md` format (YAML frontmatter + progressive disclosure instructions).
3. Include helper scripts under `scripts/` (supporting both POSIX `sh` and PowerShell where applicable).
4. Register the new plugin in `.claude-plugin/marketplace.json`.

---

© Fulltech Engineering. All rights reserved.

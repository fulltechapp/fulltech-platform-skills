# Fulltech Platform Skills

<p align="center">
  <strong>🌐 Multi-Language Documentation</strong><br>
  <a href="README.md"><b>English</b></a> •
  <a href="README.pt-BR.md"><b>Português (Brasil)</b></a> •
  <a href="README.es.md"><b>Español</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Architecture-Multi--Harness-blue?style=flat-square" alt="Multi-Harness" />
  <img src="https://img.shields.io/badge/Claude%20Code-Compatible-8A2BE2?style=flat-square" alt="Claude Code" />
  <img src="https://img.shields.io/badge/Google%20Antigravity-Compatible-4285F4?style=flat-square" alt="Google Antigravity" />
  <img src="https://img.shields.io/badge/skills.sh-Ecosystem-green?style=flat-square" alt="Skills.sh" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square" alt="License" />
</p>

---

> **Enterprise-grade Multi-Harness Agent Skills, DevOps & Engineering Marketplace for Fulltech.**

This repository hosts production-ready, modular skills designed to work seamlessly across modern AI coding agents and harnesses, including **Claude Code**, **Google Antigravity**, **Cursor**, **OpenAI Codex**, and **Orca**.

---

## 📦 Skills Directory

| Skill | Category | Description | Supported Harnesses |
| :--- | :--- | :--- | :--- |
| [`android-sanitizer`](./plugins/android-sanitizer/) | Utilities / Mobile | Autonomous Android triage, adware remediation, OEM bloatware removal (Xiaomi, Samsung, Motorola, Transsion), and Private DNS ad-sinkhole automation. | Claude Code, Antigravity, Cursor, Codex, Orca |

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
```

### 2. In Google Antigravity / Agentic Environments
Clone or copy the skill directory into your user or project agents directory:
```bash
# Global user level (available across all workspaces)
cp -r plugins/android-sanitizer ~/.agents/skills/
```

### 3. Via Open Skills CLI (`skills.sh`)
```bash
npx skills add fulltechapp/fulltech-platform-skills@android-sanitizer
```

---

## 🛠️ Repository Architecture

This repository adopts a **hybrid multi-harness standard**:

```text
fulltech-platform-skills/
├── .claude-plugin/
│   └── marketplace.json            # Claude Code / Claude Hub catalog index
├── plugins/
│   └── android-sanitizer/          # Autonomous Android triage skill
│       ├── .claude-plugin/
│       │   └── plugin.json         # Claude plugin descriptor
│       ├── SKILL.md                # Universal multi-harness agent instructions
│       ├── scripts/
│       │   ├── triage.sh           # POSIX bash helper
│       │   └── triage.ps1          # Windows PowerShell helper
│       └── references/
│           └── oem_catalog.json    # Vendor ad engines & bloatware database
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

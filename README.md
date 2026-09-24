# Fulltech Platform Skills

> **Multi-Harness Agent Skills, DevOps & Engineering Marketplace for Fulltech.**

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
/plugin marketplace add diogofrj/fulltech-platform-skills
```
Install the desired plugin:
```bash
/plugin install android-sanitizer
```

### 2. In Google Antigravity / Agentic Environments
Clone or symlink the skill directory into your user or project agents directory:
```bash
# User-level (available across all workspaces)
cp -r plugins/android-sanitizer ~/.agents/skills/
```

### 3. Via Open Skills CLI (`skills.sh`)
```bash
npx skills add diogofrj/fulltech-platform-skills@android-sanitizer
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
└── README.md
```

---

## 🤝 Contributing

1. Create a new skill directory under `plugins/<skill-name>`.
2. Follow the standard `SKILL.md` format (YAML frontmatter + progressive disclosure instructions).
3. Include helper scripts under `scripts/` (supporting both POSIX `sh` and PowerShell where applicable).
4. Register the new plugin in `.claude-plugin/marketplace.json`.

---

© Fulltech Engineering. All rights reserved.

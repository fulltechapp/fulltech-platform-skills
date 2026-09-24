# Fulltech Platform Skills - Guidelines & Context

## Project Architecture
This repository contains multi-harness agent skills and plugins for device forensics, optimization, and adware remediation across Android and iOS.

- `plugins/android-sanitizer`: ADB-based forensics, Sleep-of-Death (`mm-pp-dpps`) diagnosis, OEM catalog, and Private DNS sinkhole.
- `plugins/ios-sanitizer`: Apple Lockdown protocol (`pymobiledevice3` v11+ async), BMS raw battery register extraction (cycles, capacity, temperature), Apple CPU Dynamic Throttling detection, `/Panics` inspection, residual app purge, and native Apple `.mobileconfig` DNS sinkhole.
- `generate_report.py`: Standalone HTML artifact generator using the official **fulltech.app Design System** (Geist/JetBrains Mono, `#090A0F` background, `#11131A` cards, `#10B981` emerald, `#38BDF8` cyan). Focused on human-readable consultative verdicts.

## Connected Systems
- **FTM MCP Server:** `https://ftm.fulltech.app/mcp`
- **Supported Harnesses:** Claude Code, Google Antigravity, Cursor, OpenAI Codex, Orca.

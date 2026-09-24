---
name: windows-sanitizer
description: Autonomous Windows PC triage, telemetry deactivation, bloatware uninstallation, and performance forensics.
---

# Windows Sanitizer

Autonomous Windows PC triage, telemetry deactivation, OEM bloatware cleaner, and system-wide ad-blocking. Optimized for multi-harness agents (Antigravity, Claude Code, Codex, Cursor, Orca) to bring a system back to its peak performance without destructive changes.

## Features
- **Forensic Triage**: Analyzes CPU thermals (if available), disk health, startup impact, and RAM usage.
- **Telemetry Deactivation**: Safely disables intrusive Windows telemetry and diagnostic tracking.
- **Bloatware Removal**: Identifies and removes unnecessary pre-installed UWP apps (Candy Crush, McAfee, etc.).
- **Network Sinkhole**: Modifies the system `hosts` file to block telemetry and ad-tracking domains at the OS level.
- **HTML Reporting**: Generates an executive-style HTML report detailing system health and actions taken.

## Usage

Agents should execute the PowerShell scripts directly to perform triage and remediation.

### 1. Triage (Read-Only Analysis)
Run the triage script to generate a system health report:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\triage.ps1
```

### 2. Remediation (Interactive Action)
Run the remediation script to apply fixes (requires Administrator privileges):
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\remediate.ps1
```

### 3. WSL2 disks (optional)
Triage reports each WSL distro and its `ext4.vhdx` size under `WSL`. To reclaim space the virtual disk never returns to Windows on its own (runs `wsl --shutdown`, then `Optimize-VHD` or `diskpart compact vdisk`):
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\remediate.ps1 -CompactWslDisks
```
For cleanup inside the distro, use `linux-sanitizer`.

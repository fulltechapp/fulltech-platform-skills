#!/usr/bin/env bash
# Linux / WSL forensic triage (read-only). Writes a JSON report; never modifies the system.
set -euo pipefail

OUTPUT="./linux_triage.json"
while [[ $# -gt 0 ]]; do
    case "$1" in
        -o|--output) OUTPUT="$2"; shift 2 ;;
        -h|--help) echo "Uso: $0 [--output arquivo.json]"; exit 0 ;;
        *) echo "Argumento desconhecido: $1" >&2; exit 1 ;;
    esac
done

echo "[*] Iniciando Triage Forense no Linux..."

have() { command -v "$1" >/dev/null 2>&1; }

jstr() {
    local s=${1//\\/\\\\}
    s=${s//\"/\\\"}
    s=${s//$'\t'/\\t}
    s=${s//$'\r'/}
    s=${s//$'\n'/\\n}
    printf '"%s"' "$s"
}

jarr() {
    local out="" x
    for x in "$@"; do out+="${out:+,}$(jstr "$x")"; done
    printf '[%s]' "$out"
}

jbool() { if "$@"; then echo true; else echo false; fi; }

# Size in MB, or null when the path is missing. Unreadable subdirs are skipped (value is a lower bound).
du_mb() {
    local v=""
    [[ -e $1 ]] || { echo null; return; }
    v=$(du -sm "$1" 2>/dev/null | awk '{print $1}') || true
    echo "${v:-null}"
}

pkg_installed() { dpkg-query -W -f='${Status}' "$1" 2>/dev/null | grep -q 'install ok installed'; }

# 1. Environment
OSREL=$(cat /proc/sys/kernel/osrelease 2>/dev/null || uname -r)
VIRT=$(systemd-detect-virt 2>/dev/null || true)
if [[ -e /proc/sys/fs/binfmt_misc/WSLInterop ]] || [[ ${OSREL,,} == *microsoft* ]]; then
    if [[ $OSREL == *WSL2* ]]; then ENVIRONMENT=wsl2; else ENVIRONMENT=wsl1; fi
elif [[ -e /.dockerenv ]] || systemd-detect-virt -c -q 2>/dev/null; then
    ENVIRONMENT=container
elif [[ -n $VIRT && $VIRT != none ]]; then
    ENVIRONMENT=vm
else
    ENVIRONMENT=baremetal
fi
IS_WSL=false; [[ $ENVIRONMENT == wsl* ]] && IS_WSL=true
SYSTEMD_PID1=$(jbool test "$(ps -p 1 -o comm= 2>/dev/null)" = systemd)
HAS_APT=$(jbool have apt-get)

# 2. System
# shellcheck source=/dev/null
OS_NAME=$( (. /etc/os-release 2>/dev/null && echo "${PRETTY_NAME:-unknown}") || echo unknown)
CPU=$(grep -m1 'model name' /proc/cpuinfo 2>/dev/null | cut -d: -f2 | sed 's/^ *//' || true)
CORES=$(nproc 2>/dev/null || echo null)
read -r MEM_TOTAL MEM_AVAIL SWAP_TOTAL SWAP_FREE < <(awk '
    /^MemTotal:/{t=$2} /^MemAvailable:/{a=$2} /^SwapTotal:/{st=$2} /^SwapFree:/{sf=$2}
    END{printf "%d %d %d %d\n", t/1024, a/1024, st/1024, sf/1024}' /proc/meminfo)
read -r DISK_TOTAL DISK_FREE DISK_USED_PCT < <(df -Pm / | awk 'NR==2{gsub("%","",$5); print $2, $4, $5}')

# Thermals only make sense on real hardware
MAX_TEMP=null
if [[ $ENVIRONMENT == baremetal ]]; then
    t=$(cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null | sort -n | tail -1 || true)
    [[ -n $t ]] && MAX_TEMP=$((t / 1000))
fi

# 3. Reclaimable space
APT_CACHE_MB=$(du_mb /var/cache/apt/archives)
JOURNAL_MB=$(du_mb /var/log/journal)
VARLOG_MB=$(du_mb /var/log)
USER_CACHE_MB=$(du_mb "$HOME/.cache")
TRASH_MB=$(du_mb "$HOME/.local/share/Trash")

DISABLED_SNAPS=()
if have snap; then
    mapfile -t DISABLED_SNAPS < <(snap list --all 2>/dev/null | awk '/disabled/{print $1 " rev " $3}')
fi

DOCKER_PRESENT=$(jbool have docker)
DOCKER_RECLAIMABLE=()
if have docker; then
    # docker system df can take minutes on hosts with large volumes
    mapfile -t DOCKER_RECLAIMABLE < <(timeout 30 docker system df --format '{{.Type}}: {{.Reclaimable}}' 2>/dev/null || true)
    [[ ${#DOCKER_RECLAIMABLE[@]} -eq 0 ]] && DOCKER_RECLAIMABLE=("indisponivel (timeout ou sem permissao)")
fi

# 4. Packages
UPGRADABLE=null; SECURITY_UPGRADABLE=null; AUTOREMOVABLE=null
if have apt-get; then
    SIM=$(apt-get -s upgrade 2>/dev/null || true)
    UPGRADABLE=$(grep -c '^Inst' <<<"$SIM" || true)
    SECURITY_UPGRADABLE=$(grep '^Inst' <<<"$SIM" | grep -ci 'security' || true)
    AUTOREMOVABLE=$(apt-get -s autoremove 2>/dev/null | grep -c '^Remv' || true)
fi

# 5. Services (systemd only; WSL without systemd and containers skip this)
FAILED_UNITS=(); ENABLED_SERVICES=null
if [[ $SYSTEMD_PID1 == true ]]; then
    mapfile -t FAILED_UNITS < <(systemctl --failed --no-legend --plain 2>/dev/null | awk '{print $1}')
    ENABLED_SERVICES=$(systemctl list-unit-files --type=service --state=enabled --no-legend 2>/dev/null | wc -l)
fi

# 6. Telemetry
TELEMETRY_PKGS=()
if have dpkg-query; then
    for p in popularity-contest ubuntu-report apport whoopsie; do
        pkg_installed "$p" && TELEMETRY_PKGS+=("$p")
    done
fi
MOTD_NEWS=$(jbool grep -qs '^ENABLED=1' /etc/default/motd-news)
SINKHOLE_ENTRIES=$(grep -cE '^0\.0\.0\.0[[:space:]]' /etc/hosts 2>/dev/null || true)
SINKHOLE_ENTRIES=${SINKHOLE_ENTRIES:-0}

# 7. WSL specifics
WSL_JSON=null
if [[ $IS_WSL == true ]]; then
    wslconf() { # value of a key in /etc/wsl.conf, or "default"
        local v
        v=$(grep -iE "^[[:space:]]*$1[[:space:]]*=" /etc/wsl.conf 2>/dev/null | tail -1 | cut -d= -f2 | tr -d '[:space:]' || true)
        echo "${v:-default}"
    }
    WIN_PATH_ENTRIES=$(tr ':' '\n' <<<"$PATH" | grep -c '^/mnt/' || true)
    shopt -s nullglob
    WSLCONFIGS=()
    for f in /mnt/c/Users/*/.wslconfig; do WSLCONFIGS+=("$f: $(grep -iE '^[[:space:]]*(memory|swap|processors)[[:space:]]*=' "$f" | tr -d '\r' | paste -sd ';' - || true)"); done
    shopt -u nullglob
    WSL_JSON=$(cat <<EOF
{
    "Systemd": $(jstr "$(wslconf systemd)"),
    "GenerateHosts": $(jstr "$(wslconf generateHosts)"),
    "AppendWindowsPath": $(jstr "$(wslconf appendWindowsPath)"),
    "WindowsPathEntries": $WIN_PATH_ENTRIES,
    "WslConfigFiles": $(jarr "${WSLCONFIGS[@]}")
  }
EOF
)
fi

cat >"$OUTPUT" <<EOF
{
  "Environment": {
    "Type": $(jstr "$ENVIRONMENT"),
    "Virtualization": $(jstr "${VIRT:-none}"),
    "SystemdPid1": $SYSTEMD_PID1,
    "AptAvailable": $HAS_APT
  },
  "System": {
    "OS": $(jstr "$OS_NAME"),
    "Kernel": $(jstr "$OSREL"),
    "CPU": $(jstr "${CPU:-unknown}"),
    "Cores": $CORES,
    "RamTotalMB": $MEM_TOTAL,
    "RamAvailableMB": $MEM_AVAIL,
    "SwapTotalMB": $SWAP_TOTAL,
    "SwapFreeMB": $SWAP_FREE,
    "MaxThermalC": $MAX_TEMP
  },
  "Disk": {
    "RootTotalMB": $DISK_TOTAL,
    "RootFreeMB": $DISK_FREE,
    "RootUsedPercent": $DISK_USED_PCT,
    "AptCacheMB": $APT_CACHE_MB,
    "JournalMB": $JOURNAL_MB,
    "VarLogMB": $VARLOG_MB,
    "UserCacheMB": $USER_CACHE_MB,
    "TrashMB": $TRASH_MB,
    "DisabledSnapRevisions": $(jarr "${DISABLED_SNAPS[@]}"),
    "DockerPresent": $DOCKER_PRESENT,
    "DockerReclaimable": $(jarr "${DOCKER_RECLAIMABLE[@]}")
  },
  "Packages": {
    "Upgradable": $UPGRADABLE,
    "SecurityUpgradable": $SECURITY_UPGRADABLE,
    "Autoremovable": $AUTOREMOVABLE
  },
  "Services": {
    "Failed": $(jarr "${FAILED_UNITS[@]}"),
    "EnabledCount": $ENABLED_SERVICES
  },
  "Security": {
    "TelemetryPackages": $(jarr "${TELEMETRY_PKGS[@]}"),
    "MotdNewsEnabled": $MOTD_NEWS,
    "HostsSinkholeEntries": $SINKHOLE_ENTRIES
  },
  "WSL": $WSL_JSON
}
EOF

echo "[+] Triage concluido! Dados salvos em $OUTPUT"

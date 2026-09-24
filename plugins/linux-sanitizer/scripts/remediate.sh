#!/usr/bin/env bash
# Linux / WSL remediation. Dry-run by default: only prints what would be done.
# --apply executes (root required), asking S/N per action unless --yes or explicit action flags are given.
set -euo pipefail

APPLY=false; AUTO=false; EXPLICIT=false
declare -A FLAG=()
usage() {
    cat <<EOF
Uso: $0 [--apply] [--yes] [acoes...]
  --apply              executa de verdade (padrao: dry-run)
  --yes                confirma todas as acoes sem perguntar
Acoes (se nenhuma for passada, todas as aplicaveis sao oferecidas):
  --clean-packages     apt-get clean + autoremove
  --vacuum-journal     reduz o journal do systemd para 200M
  --prune-snaps        remove revisoes desativadas de snaps
  --disable-telemetry  desativa apport, whoopsie, popularity-contest, ubuntu-report e motd-news
  --hosts-sinkhole     bloqueia dominios de telemetria do Ubuntu em /etc/hosts
  --wsl-windows-path   (WSL) appendWindowsPath=false em /etc/wsl.conf
EOF
}
while [[ $# -gt 0 ]]; do
    case "$1" in
        --apply) APPLY=true ;;
        --yes) AUTO=true ;;
        --clean-packages|--vacuum-journal|--prune-snaps|--disable-telemetry|--hosts-sinkhole|--wsl-windows-path)
            FLAG[${1#--}]=1; EXPLICIT=true ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Argumento desconhecido: $1" >&2; usage >&2; exit 1 ;;
    esac
    shift
done

if [[ $APPLY == true && $EUID -ne 0 ]]; then
    echo "[!] --apply requer root. Execute com sudo." >&2
    exit 1
fi

have() { command -v "$1" >/dev/null 2>&1; }

# Mirrors Should-Run in windows-sanitizer/scripts/remediate.ps1
should_run() {
    local question=$1 key=$2 answer
    [[ -n ${FLAG[$key]:-} ]] && return 0
    [[ $EXPLICIT == true ]] && return 1
    [[ $APPLY == false || $AUTO == true ]] && return 0
    read -r -p "$question [S/N] " answer
    [[ $answer =~ ^[sS]$ ]]
}

RAN=0
run() {
    RAN=$((RAN + 1))
    if [[ $APPLY == true ]]; then echo "  + $*"; "$@"; else echo "  [dry-run] $*"; fi
}

OSREL=$(cat /proc/sys/kernel/osrelease 2>/dev/null || uname -r)
IS_WSL=false
[[ -e /proc/sys/fs/binfmt_misc/WSLInterop || ${OSREL,,} == *microsoft* ]] && IS_WSL=true

if [[ $APPLY == true ]]; then
    echo "[*] Iniciando Remediacao do Linux..."
else
    echo "[*] Dry-run: nada sera alterado. Use --apply para executar."
fi

# 1. Package cache
echo; echo "[1] Cache de pacotes (apt)"
if ! have apt-get; then
    echo "  [-] apt nao disponivel; ignorado."
elif should_run "Limpar cache do apt e remover pacotes orfaos?" clean-packages; then
    run apt-get clean
    run apt-get -y autoremove
else
    echo "  [-] Ignorado."
fi

# 2. Journal
echo; echo "[2] Journal do systemd"
if ! have journalctl || [[ ! -d /var/log/journal ]]; then
    echo "  [-] Journal persistente nao encontrado; ignorado."
elif should_run "Reduzir o journal para 200M?" vacuum-journal; then
    run journalctl --vacuum-size=200M
else
    echo "  [-] Ignorado."
fi

# 3. Snap revisions
echo; echo "[3] Revisoes antigas de snaps"
DISABLED=()
have snap && mapfile -t DISABLED < <(snap list --all 2>/dev/null | awk '/disabled/{print $1 " " $3}')
if [[ ${#DISABLED[@]} -eq 0 ]]; then
    echo "  [-] Nenhuma revisao desativada."
elif should_run "Remover ${#DISABLED[@]} revisoes desativadas de snaps?" prune-snaps; then
    for entry in "${DISABLED[@]}"; do
        run snap remove "${entry% *}" --revision="${entry#* }"
    done
else
    echo "  [-] Ignorado."
fi

# 4. Telemetry: disabled, not purged. Purging these removes ubuntu-standard/ubuntu-desktop
# metapackages and a later autoremove could then take out unrelated packages.
echo; echo "[4] Telemetria"
if should_run "Desativar apport, whoopsie, popularity-contest, ubuntu-report e motd-news?" disable-telemetry; then
    RAN_BEFORE=$RAN
    if [[ -f /etc/default/apport ]]; then
        run sed -i 's/^enabled=1/enabled=0/' /etc/default/apport
    fi
    for svc in apport.service whoopsie.service; do
        if have systemctl && systemctl list-unit-files "$svc" --no-legend 2>/dev/null | grep -q .; then
            run systemctl disable --now "$svc"
        fi
    done
    if [[ -f /etc/popularity-contest.conf ]]; then
        run sed -i 's/^PARTICIPATE=.*/PARTICIPATE="no"/' /etc/popularity-contest.conf
    fi
    if have ubuntu-report; then
        run ubuntu-report -f send no
    fi
    if [[ -f /etc/default/motd-news ]]; then
        run sed -i 's/^ENABLED=1/ENABLED=0/' /etc/default/motd-news
    fi
    [[ $RAN -eq $RAN_BEFORE ]] && echo "  [*] Nada a desativar."
else
    echo "  [-] Ignorado."
fi

# 5. Hosts sinkhole
echo; echo "[5] Ad-Sinkhole Local (/etc/hosts)"
GENERATE_HOSTS=$(grep -iE '^[[:space:]]*generateHosts[[:space:]]*=' /etc/wsl.conf 2>/dev/null | tail -1 | cut -d= -f2 | tr -d '[:space:]' || true)
if [[ $IS_WSL == true && ${GENERATE_HOSTS,,} != false ]]; then
    echo "  [!] WSL regenera /etc/hosts a partir do hosts do Windows (generateHosts=true)."
    echo "      A alteracao seria perdida. Aplique o sinkhole no Windows com windows-sanitizer."
elif should_run "Adicionar bloqueio de telemetria do Ubuntu no /etc/hosts?" hosts-sinkhole; then
    SINKHOLE=(
        "0.0.0.0 metrics.ubuntu.com"
        "0.0.0.0 popcon.ubuntu.com"
        "0.0.0.0 daisy.ubuntu.com"
        "0.0.0.0 motd.ubuntu.com"
    )
    MISSING=()
    for entry in "${SINKHOLE[@]}"; do
        grep -qxF "$entry" /etc/hosts || MISSING+=("$entry")
    done
    if [[ ${#MISSING[@]} -eq 0 ]]; then
        echo "  [*] Todas as entradas de sinkhole ja estavam presentes no hosts."
    else
        run sh -c 'printf "\n# fulltech linux-sanitizer\n" >> /etc/hosts'
        for entry in "${MISSING[@]}"; do
            run sh -c "echo '$entry' >> /etc/hosts"
        done
    fi
else
    echo "  [-] Ignorado."
fi

# 6. WSL: Windows PATH appended to the Linux PATH slows down command lookup
if [[ $IS_WSL == true ]]; then
    echo; echo "[6] WSL: PATH do Windows"
    if grep -qiE '^[[:space:]]*appendWindowsPath[[:space:]]*=[[:space:]]*false' /etc/wsl.conf 2>/dev/null; then
        echo "  [*] appendWindowsPath ja esta false."
    elif should_run "Definir appendWindowsPath=false em /etc/wsl.conf?" wsl-windows-path; then
        if grep -qiE '^[[:space:]]*appendWindowsPath[[:space:]]*=' /etc/wsl.conf 2>/dev/null; then
            run sed -i -E 's/^[[:space:]]*appendWindowsPath[[:space:]]*=.*/appendWindowsPath=false/I' /etc/wsl.conf
        elif grep -qiE '^\[interop\]' /etc/wsl.conf 2>/dev/null; then
            run sed -i -E '/^\[interop\]/I a appendWindowsPath=false' /etc/wsl.conf
        else
            run sh -c 'printf "\n[interop]\nappendWindowsPath=false\n" >> /etc/wsl.conf'
        fi
        echo "  [i] Vale apos 'wsl --shutdown' no Windows."
    else
        echo "  [-] Ignorado."
    fi
fi

echo; echo "[+] Higienizacao do Linux concluida!"

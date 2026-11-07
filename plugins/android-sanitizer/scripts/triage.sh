#!/usr/bin/env bash
# Android Sanitizer - Automated ADB Triage & Diagnostic Helper (Bash)

set -e

color_cyan="\033[0;36m"
color_yellow="\033[1;33m"
color_green="\033[0;32m"
color_red="\033[0;31m"
color_reset="\033[0m"

log_section() {
    echo -e "\n${color_cyan}=== $1 ===${color_reset}"
}

if ! command -v adb &> /dev/null; then
    echo -e "${color_red}Error: adb not found in PATH.${color_reset}"
    exit 1
fi

device=$(adb devices | grep -w "device" || true)
if [ -z "$device" ]; then
    echo -e "${color_yellow}No authorized device found. Connect via USB and accept USB Debugging on phone.${color_reset}"
    adb devices
    exit 1
fi

manufacturer=$(adb shell getprop ro.product.manufacturer | tr -d '\r\n' | tr '[:upper:]' '[:lower:]')
model=$(adb shell getprop ro.product.model | tr -d '\r\n')
android_ver=$(adb shell getprop ro.build.version.release | tr -d '\r\n')
patch=$(adb shell getprop ro.build.version.security_patch | tr -d '\r\n')

log_section "Device Connected"
echo "Manufacturer:   $manufacturer"
echo "Model:          $model"
echo "Android:        $android_ver"
echo "Security Patch: $patch"

case "$1" in
    --sod|--crash-audit)
        log_section "Sleep-of-Death (SOD) & Display Crash Audit"
        sod_logs=$(adb shell "dumpsys dropbox --print" | grep -E "mm-pp-dpps|surfaceflinger|DEAD_OBJECT|system_server_crash" || true)
        if [ -n "$sod_logs" ]; then
            echo -e "${color_red}  [ALERT] Sleep-of-Death (SOD) crash markers found in Dropbox!${color_reset}"
            echo -e "${color_yellow}  Symptom: Phone appears dead with 100% battery, only waking on USB plug.${color_reset}"
            echo -e "${color_yellow}  Root Cause: Display pipeline deadlock (mm-pp-dpps/SurfaceFlinger) caused by ad overlays/video loops.${color_reset}"
            echo "$sod_logs" | head -n 5
        else
            echo -e "${color_green}  [CLEAN] No display crash or SOD deadlocks found.${color_reset}"
        fi
        exit 0
        ;;
    --health|--battery)
        log_section "Sleep-of-Death (SOD) Check"
        sod_logs=$(adb shell "dumpsys dropbox --print" | grep -E "mm-pp-dpps|surfaceflinger|DEAD_OBJECT" || true)
        if [ -n "$sod_logs" ]; then
            echo -e "${color_red}  [ALERT] Display deadlock / SOD tombstone markers detected.${color_reset}"
        fi

        log_section "Hardware & Battery Health Analysis"
        batt=$(adb shell dumpsys battery)
        level=$(echo "$batt" | grep "level:" | awk '{print $2}')
        temp_raw=$(echo "$batt" | grep "temperature:" | awk '{print $2}')
        temp=$(awk "BEGIN {print $temp_raw / 10}")
        health_code=$(echo "$batt" | grep "health:" | awk '{print $2}')
        case "$health_code" in
            2) health_str="Good (Saudável)" ;;
            3) health_str="Overheat" ;;
            4) health_str="Dead" ;;
            5) health_str="Over Voltage" ;;
            *) health_str="Unknown ($health_code)" ;;
        esac
        echo -e "${color_green}  Battery Level:       ${level}%${color_reset}"
        echo -e "${color_green}  Battery Health:      ${health_str}${color_reset}"
        echo "  Battery Temperature: ${temp} °C"

        stats=$(adb shell "dumpsys batterystats --charged" || true)
        est_cap=$(echo "$stats" | grep "Estimated battery capacity:" | awk '{print $4}' || true)
        if [ -n "$est_cap" ]; then
            echo "  Estimated Capacity:  ${est_cap} mAh"
        fi

        log_section "Storage & Memory (/data)"
        adb shell df -h /data
        adb shell dumpsys meminfo | grep -E "Total RAM:|Free RAM:|Used RAM:"
        exit 0
        ;;
    --watch)
        log_section "Watching Active Top Window (Ctrl+C to stop)"
        while true; do
            focus=$(adb shell "dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'")
            echo -e "${color_yellow}[$(date +%T)] $focus${color_reset}"
            sleep 1
        done
        ;;
    --dns-open)
        log_section "Opening Private DNS Settings"
        adb shell am start -W -a android.settings.WIRELESS_SETTINGS
        echo -e "${color_green}Settings screen opened on phone. Instruct user to type 'dns.adguard-dns.com'.${color_reset}"
        exit 0
        ;;
    --dns-test)
        log_section "Testing Ad-Sinkhole Resolution"
        mode=$(adb shell settings get global private_dns_mode | tr -d '\r\n')
        spec=$(adb shell settings get global private_dns_specifier | tr -d '\r\n')
        echo "Private DNS Mode: $mode"
        echo "DNS Hostname:     $spec"
        echo "Pinging test ad domain (pagead2.googlesyndication.com)..."
        adb shell "ping -c 1 pagead2.googlesyndication.com"
        exit 0
        ;;
esac

log_section "Apps with Overlay Permission (SYSTEM_ALERT_WINDOW)"
adb shell "cmd appops query-op SYSTEM_ALERT_WINDOW allow"

log_section "Installed WebAPKs (Browser-installed apps)"
webapks=$(adb shell "pm list packages | grep webapk" || true)
if [ -n "$webapks" ]; then
    echo -e "${color_yellow}$webapks${color_reset}"
else
    echo "  None found."
fi

log_section "User-Installed 3rd-Party Packages"
adb shell "pm list packages -3"

log_section "Private DNS Status"
spec=$(adb shell settings get global private_dns_specifier | tr -d '\r\n')
if [[ "$spec" == *"adguard"* ]]; then
    echo -e "${color_green}  [PROTECTED] Private DNS is set to $spec${color_reset}"
else
    echo -e "${color_red}  [UNPROTECTED] Current DNS specifier: $spec${color_reset}"
fi

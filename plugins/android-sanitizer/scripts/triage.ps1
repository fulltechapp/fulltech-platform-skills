<#
.SYNOPSIS
    Android Sanitizer - Automated ADB Triage & Diagnostic Helper (PowerShell)
.DESCRIPTION
    Audits connected Android device for adware, overlay abusers, vendor ad services,
    and checks Private DNS status.
#>

[CmdletBinding()]
param(
    [switch]$WatchOverlay,
    [switch]$OpenDnsSettings,
    [switch]$TestDns
)

function Write-Section($title) {
    Write-Host "`n=== $title ===" -ForegroundColor Cyan
}

# Check ADB
if (-not (Get-Command adb -ErrorAction SilentlyContinue)) {
    Write-Error "ADB not found in PATH. Please install Android Platform Tools."
    exit 1
}

$device = adb devices | Select-String -Pattern "\bdevice\b"
if (-not $device) {
    Write-Warning "No authorized device connected. Please plug device via USB and accept USB Debugging."
    adb devices
    exit 1
}

$manufacturer = (adb shell getprop ro.product.manufacturer).Trim().ToLower()
$model = (adb shell getprop ro.product.model).Trim()
$androidVer = (adb shell getprop ro.build.version.release).Trim()

Write-Section "Device Connected"
Write-Host "Manufacturer: $manufacturer"
Write-Host "Model:        $model"
Write-Host "Android:      $androidVer"

if ($WatchOverlay) {
    Write-Section "Watching Active Top Window (Ctrl+C to stop)"
    while ($true) {
        $focus = adb shell "dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'"
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $focus" -ForegroundColor Yellow
        Start-Sleep -Seconds 1
    }
    exit 0
}

if ($OpenDnsSettings) {
    Write-Section "Opening Private DNS Settings Screen"
    adb shell am start -W -a android.settings.WIRELESS_SETTINGS
    Write-Host "Settings screen opened on phone. Instruct user to set 'dns.adguard-dns.com'." -ForegroundColor Green
    exit 0
}

if ($TestDns) {
    Write-Section "Testing Ad-Sinkhole Resolution"
    $mode = (adb shell settings get global private_dns_mode).Trim()
    $specifier = (adb shell settings get global private_dns_specifier).Trim()
    Write-Host "Private DNS Mode: $mode"
    Write-Host "DNS Hostname:     $specifier"
    Write-Host "Pinging ad test target (pagead2.googlesyndication.com)..."
    adb shell "ping -c 1 pagead2.googlesyndication.com"
    exit 0
}

# 1. Overlay Check
Write-Section "Apps with Overlay Permission (SYSTEM_ALERT_WINDOW)"
$overlays = adb shell "cmd appops query-op SYSTEM_ALERT_WINDOW allow"
$overlays | ForEach-Object { Write-Host "  $_" -ForegroundColor Yellow }

# 2. WebAPKs
Write-Section "Installed WebAPKs (Browser-installed apps)"
$webapks = adb shell "pm list packages | grep webapk"
if ($webapks) {
    $webapks | ForEach-Object { Write-Host "  $_" -ForegroundColor Magenta }
} else {
    Write-Host "  None found." -ForegroundColor Gray
}

# 3. Third-party Apps
Write-Section "User-Installed 3rd-Party Packages"
$thirdParty = adb shell "pm list packages -3"
$thirdParty | ForEach-Object { Write-Host "  $_" }

# 4. DNS Status
Write-Section "Private DNS Status"
$mode = (adb shell settings get global private_dns_mode).Trim()
$specifier = (adb shell settings get global private_dns_specifier).Trim()
if ($specifier -like "*adguard*") {
    Write-Host "  [PROTECTED] Private DNS is set to $specifier" -ForegroundColor Green
} else {
    Write-Host "  [UNPROTECTED] Current mode: $mode, specifier: $specifier" -ForegroundColor Red
}

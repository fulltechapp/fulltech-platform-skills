<#
.SYNOPSIS
    Android Sanitizer - Automated ADB Triage & Diagnostic Helper (PowerShell)
.DESCRIPTION
    Audits connected Android device for adware, overlay abusers, vendor ad services,
    battery health, hardware lifespan, Sleep-of-Death (SOD) crashes, and Private DNS status.
#>

[CmdletBinding()]
param(
    [switch]$WatchOverlay,
    [switch]$OpenDnsSettings,
    [switch]$TestDns,
    [switch]$HealthCheck,
    [switch]$AuditSOD
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
$patch = (adb shell getprop ro.build.version.security_patch).Trim()

Write-Section "Device Connected"
Write-Host "Manufacturer:   $manufacturer"
Write-Host "Model:          $model"
Write-Host "Android:        $androidVer"
Write-Host "Security Patch: $patch"

# Sleep of Death (SOD) & Crash Audit
if ($AuditSOD -or $HealthCheck) {
    Write-Section "Sleep-of-Death (SOD) & Display Crash Audit"
    $sodLogs = adb shell "dumpsys dropbox --print" | Select-String -Pattern "mm-pp-dpps|surfaceflinger|DEAD_OBJECT|system_server_crash"
    if ($sodLogs) {
        Write-Host "  [ALERT] Sleep-of-Death (SOD) crash markers found in Dropbox!" -ForegroundColor Red
        Write-Host "  Symptom: Phone appears dead with 100% battery, only waking on USB plug." -ForegroundColor Yellow
        Write-Host "  Root Cause: Display pipeline deadlock (mm-pp-dpps/SurfaceFlinger) caused by ad overlays/video loops." -ForegroundColor Yellow
        $sodLogs | Select-Object -First 4 | ForEach-Object { Write-Host "    $($_.Line.Trim())" -ForegroundColor DarkYellow }
    } else {
        Write-Host "  [CLEAN] No display crash or SOD deadlocks found." -ForegroundColor Green
    }
}

if ($HealthCheck) {
    Write-Section "Hardware & Battery Health Analysis"
    
    # 1. Battery metrics
    $batt = adb shell "dumpsys battery"
    $level = ($batt | Select-String "\blevel:\s*(\d+)").Matches.Groups[1].Value
    $voltageRaw = ($batt | Select-String "\bvoltage:\s*(\d+)").Matches.Groups[1].Value
    $voltage = if ($voltageRaw) { [double]$voltageRaw / 1000 } else { 0 }
    $tempRaw = ($batt | Select-String "\btemperature:\s*(\d+)").Matches.Groups[1].Value
    $temp = if ($tempRaw) { [double]$tempRaw / 10 } else { 0 }
    $healthCode = ($batt | Select-String "\bhealth:\s*(\d+)").Matches.Groups[1].Value
    $healthMap = @{"1"="Unknown"; "2"="Good (Saudável)"; "3"="Overheat"; "4"="Dead"; "5"="Over Voltage"; "6"="Failure"; "7"="Cold"}
    $healthStr = if ($healthMap.ContainsKey($healthCode)) { $healthMap[$healthCode] } else { "Unknown" }

    $stats = adb shell "dumpsys batterystats --charged"
    $estCap = ($stats | Select-String "Estimated battery capacity:\s*(\d+)\s*mAh").Matches.Groups[1].Value
    $desCap = ($stats | Select-String "Capacity:\s*(\d+)").Matches.Groups[1].Value
    if (-not $desCap) { $desCap = 4000 }
    $healthPct = if ($estCap -and [int]$desCap -gt 0) { [math]::Round(([double]$estCap / [double]$desCap) * 100, 1) } else { "N/A" }

    Write-Host "  Battery Level:        $level%" -ForegroundColor Green
    Write-Host "  Battery Health:       $healthStr" -ForegroundColor Green
    Write-Host "  Battery Voltage:      $voltage V"
    Write-Host "  Battery Temperature:  $temp °C"
    Write-Host "  Estimated Capacity:   $estCap mAh (Design: $desCap mAh)"
    Write-Host "  Battery Health Ratio: $healthPct%" -ForegroundColor $(if ($healthPct -ge 80) { "Green" } else { "Yellow" })

    # 2. Thermal status
    $thermal = adb shell "dumpsys thermalservice"
    $tStatus = ($thermal | Select-String "Thermal Status:\s*(\d+)").Matches.Groups[1].Value
    $tMap = @{"0"="Normal (Sem estrangulamento térmico)"; "1"="Light Throttling"; "2"="Moderate"; "3"="Severe"; "4"="Critical"}
    $tStatusStr = if ($tMap.ContainsKey($tStatus)) { $tMap[$tStatus] } else { "Normal" }
    Write-Host "  Thermal Status:       $tStatusStr" -ForegroundColor Green

    # 3. Storage
    $df = adb shell "df -h /data" | Select-Object -Skip 1
    $sParts = ($df.Trim() -split "\s+")
    Write-Host "  Storage /data:        $($sParts[2]) usado de $($sParts[1]) ($($sParts[3]) livre, $($sParts[4]) ocupado)"

    # 4. RAM
    $mem = adb shell "dumpsys meminfo" | Select-String "Total RAM:|Free RAM:|Used RAM:"
    $mem | ForEach-Object { Write-Host "  $($_.Line.Trim())" }
    exit 0
}

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

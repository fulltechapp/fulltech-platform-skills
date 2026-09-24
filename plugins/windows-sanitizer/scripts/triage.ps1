param (
    [string]$OutputPath = ".\windows_triage.json"
)

Write-Host "[*] Iniciando Triage Forense no Windows..." -ForegroundColor Cyan

# 1. OS & System Info
$os = Get-CimInstance Win32_OperatingSystem
$cpu = Get-CimInstance Win32_Processor
$ram = Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum
$ramGB = [math]::Round($ram.Sum / 1GB, 2)

# 2. Disk Health (System Drive)
$disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
$diskTotal = [math]::Round($disk.Size / 1GB, 2)
$diskFree = [math]::Round($disk.FreeSpace / 1GB, 2)
$diskPercent = [math]::Round(($diskFree / $diskTotal) * 100, 2)

# 3. Startup Apps Impact
$startupApps = Get-CimInstance Win32_StartupCommand | Select-Object Name, Command | Measure-Object | Select-Object -ExpandProperty Count

# 4. Known Bloatware Detection (UWP)
$bloatList = @(
    "Microsoft.BingWeather",
    "Microsoft.GetHelp",
    "Microsoft.Getstarted",
    "Microsoft.Messaging",
    "Microsoft.Microsoft3DViewer",
    "Microsoft.MicrosoftSolitaireCollection",
    "Microsoft.NetworkSpeedTest",
    "Microsoft.News",
    "Microsoft.Office.OneNote",
    "Microsoft.People",
    "Microsoft.Print3D",
    "Microsoft.SkypeApp",
    "Microsoft.Todos",
    "Microsoft.WindowsAlarms",
    "Microsoft.WindowsCamera",
    "microsoft.windowscommunicationsapps",
    "Microsoft.WindowsFeedbackHub",
    "Microsoft.WindowsMaps",
    "Microsoft.WindowsSoundRecorder",
    "Microsoft.Xbox.TCUI",
    "Microsoft.XboxApp",
    "Microsoft.XboxGameOverlay",
    "Microsoft.XboxGamingOverlay",
    "Microsoft.XboxIdentityProvider",
    "Microsoft.XboxSpeechToTextOverlay",
    "Microsoft.ZuneAudio",
    "Microsoft.ZuneVideo",
    "King.CandyCrushSaga",
    "SpotifyAB.SpotifyMusic"
)

$detectedBloatware = @()
foreach ($app in $bloatList) {
    if (Get-AppxPackage -Name "*$app*" -ErrorAction SilentlyContinue) {
        $detectedBloatware += $app
    }
}

# 5. Telemetry Status
$telemetryKey = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection"
$telemetryAllowed = $true
if (Test-Path $telemetryKey) {
    $val = Get-ItemProperty -Path $telemetryKey -Name "AllowTelemetry" -ErrorAction SilentlyContinue
    if ($null -ne $val -and $val.AllowTelemetry -eq 0) {
        $telemetryAllowed = $false
    }
}

# 6. WSL (host side): distros and virtual disk sizes, read from the registry
# because `wsl -l -v` prints UTF-16 that is awkward to parse
$wslInfo = $null
$lxss = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Lxss"
if (Test-Path $lxss) {
    $distros = @()
    foreach ($key in Get-ChildItem $lxss) {
        $d = Get-ItemProperty $key.PSPath
        $vhdx = Join-Path $d.BasePath "ext4.vhdx"
        $distros += @{
            Name = $d.DistributionName
            Version = $d.Version
            VhdxGB = if (Test-Path -LiteralPath $vhdx) { [math]::Round((Get-Item -LiteralPath $vhdx).Length / 1GB, 2) } else { $null }
        }
    }
    $wslConfigPath = "$env:USERPROFILE\.wslconfig"
    $wslInfo = @{
        Distros = $distros
        WslConfig = if (Test-Path $wslConfigPath) { (Get-Content $wslConfigPath | Where-Object { $_ -match '^\s*(memory|swap|processors)\s*=' }) -join '; ' } else { $null }
    }
}

# Compile Results
$results = @{
    System = @{
        OSVersion = $os.Caption
        CPU = $cpu.Name
        RAM = "$ramGB GB"
        BuildNumber = $os.BuildNumber
    }
    Disk = @{
        TotalGB = $diskTotal
        FreeGB = $diskFree
        FreePercentage = $diskPercent
    }
    Performance = @{
        StartupAppCount = $startupApps
    }
    Security = @{
        TelemetryEnabled = $telemetryAllowed
        BloatwareCount = $detectedBloatware.Count
        DetectedBloatware = $detectedBloatware
    }
    WSL = $wslInfo
}

$results | ConvertTo-Json -Depth 4 | Out-File -FilePath $OutputPath -Encoding utf8
Write-Host "[+] Triage concluido! Dados salvos em $OutputPath" -ForegroundColor Green

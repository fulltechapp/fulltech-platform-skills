param (
    [switch]$AutoConfirm,
    [switch]$DisableTelemetry,
    [switch]$RemoveBloatware,
    [switch]$ApplyHostsSinkhole,
    [switch]$CompactWslDisks,
    [string[]]$ExcludeApps = @(),
    [string]$TriagePath = ".\windows_triage.json"
)

Write-Host "[*] Iniciando Remediacao do Windows..." -ForegroundColor Cyan

# Check for Admin rights
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "[!] Este script requer privilegios de Administrador. Execute o PowerShell como Administrador." -ForegroundColor Red
    Exit
}

# Resolve triage path
if (-not (Test-Path $TriagePath)) {
    if (Test-Path "$PSScriptRoot\..\windows_triage.json") {
        $TriagePath = "$PSScriptRoot\..\windows_triage.json"
    } elseif (Test-Path ".\plugins\windows-sanitizer\windows_triage.json") {
        $TriagePath = ".\plugins\windows-sanitizer\windows_triage.json"
    }
}

# Flatten comma-delimited ExcludeApps passed via CLI
$normalizedExclude = @()
foreach ($item in $ExcludeApps) {
    if ($item -match ',') {
        $normalizedExclude += ($item -split ',').Trim()
    } elseif ($item) {
        $normalizedExclude += $item.Trim()
    }
}

$hasExplicitFlags = $DisableTelemetry -or $RemoveBloatware -or $ApplyHostsSinkhole -or $CompactWslDisks

function Should-Run {
    param([string]$ActionName, [bool]$FlagValue = $false)
    if ($FlagValue) { return $true }
    if ($hasExplicitFlags) { return $false }
    if ($AutoConfirm) { return $true }
    $response = Read-Host "$ActionName [S/N]"
    return ($response -match "^[sS]$")
}

# 1. Desativar Telemetria
Write-Host "`n[1] Auditoria de Privacidade (Telemetria)" -ForegroundColor Yellow
if (Should-Run "Deseja desativar a telemetria do Windows OS?" $DisableTelemetry) {
    Write-Host "Desativando telemetria..." -ForegroundColor Gray
    $key = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection"
    if (-not (Test-Path $key)) {
        New-Item -Path $key -Force | Out-Null
    }
    Set-ItemProperty -Path $key -Name "AllowTelemetry" -Value 0 -Type DWord
    
    # Disable tracking services
    Stop-Service -Name "DiagTrack" -ErrorAction SilentlyContinue
    Set-Service -Name "DiagTrack" -StartupType Disabled -ErrorAction SilentlyContinue
    Stop-Service -Name "dmwappushservice" -ErrorAction SilentlyContinue
    Set-Service -Name "dmwappushservice" -StartupType Disabled -ErrorAction SilentlyContinue
    Write-Host "[+] Telemetria desativada com sucesso." -ForegroundColor Green
} else {
    Write-Host "[-] Etapa de telemetria ignorada." -ForegroundColor DarkGray
}

# 2. Remover Bloatware UWP
Write-Host "`n[2] Remocao de Bloatware (UWP Apps)" -ForegroundColor Yellow
if (Test-Path $TriagePath) {
    $triageData = Get-Content $TriagePath -Raw -Encoding UTF8 | ConvertFrom-Json
    $bloatware = $triageData.Security.DetectedBloatware
    
    if ($bloatware.Count -gt 0) {
        Write-Host "Encontrados $($bloatware.Count) aplicativos de bloatware." -ForegroundColor Gray
        if (Should-Run "Deseja remover os aplicativos de bloatware detectados?" $RemoveBloatware) {
            foreach ($app in $bloatware) {
                if ($normalizedExclude -contains $app) {
                    Write-Host "[*] Mantendo aplicativo excluido pelo usuario: $app" -ForegroundColor Cyan
                    continue
                }
                Write-Host "Removendo $app..." -ForegroundColor Gray
                Get-AppxPackage -Name "*$app*" | Remove-AppxPackage -ErrorAction SilentlyContinue
            }
            Write-Host "[+] Bloatware selecionado removido com sucesso." -ForegroundColor Green
        } else {
            Write-Host "[-] Remocao de bloatware ignorada." -ForegroundColor DarkGray
        }
    } else {
        Write-Host "Nenhum bloatware conhecido detectado no arquivo de triage." -ForegroundColor Gray
    }
} else {
    Write-Host "Arquivo de triage nao encontrado ($TriagePath). Execute triage.ps1 primeiro." -ForegroundColor Red
}

# 3. Ad-Sinkhole Local (Arquivo Hosts)
Write-Host "`n[3] Ad-Sinkhole Local (Arquivo Hosts)" -ForegroundColor Yellow
if (Should-Run "Deseja adicionar regras de bloqueio de anuncios e rastreamento no arquivo Hosts?" $ApplyHostsSinkhole) {
    $hostsPath = "$env:windir\System32\drivers\etc\hosts"
    $sinkholeEntries = @(
        "0.0.0.0 vortex.data.microsoft.com",
        "0.0.0.0 vortex-win.data.microsoft.com",
        "0.0.0.0 telecommand.telemetry.microsoft.com",
        "0.0.0.0 telecommand.telemetry.microsoft.com.nsatc.net",
        "0.0.0.0 oca.telemetry.microsoft.com",
        "0.0.0.0 oca.telemetry.microsoft.com.nsatc.net",
        "0.0.0.0 sqm.telemetry.microsoft.com",
        "0.0.0.0 sqm.telemetry.microsoft.com.nsatc.net"
    )
    
    try {
        $currentHosts = Get-Content $hostsPath -Raw -ErrorAction Stop
        $linesToAdd = @()
        foreach ($entry in $sinkholeEntries) {
            if ($currentHosts -notmatch [regex]::Escape($entry)) {
                $linesToAdd += $entry
            }
        }
        if ($linesToAdd.Count -gt 0) {
            [System.IO.File]::AppendAllText($hostsPath, "`r`n" + ($linesToAdd -join "`r`n") + "`r`n")
            Write-Host "[+] $($linesToAdd.Count) entradas de sinkhole adicionadas ao hosts." -ForegroundColor Green
        } else {
            Write-Host "[*] Todas as entradas de sinkhole ja estavam presentes no hosts." -ForegroundColor Cyan
        }
    } catch {
        Write-Host "[!] Nao foi possivel editar o arquivo hosts: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "[-] Insercao no hosts ignorada." -ForegroundColor DarkGray
}

# 4. Compactar discos do WSL2 (ext4.vhdx so cresce; espaco liberado no Linux nao volta ao Windows sozinho)
Write-Host "`n[4] Discos virtuais do WSL2 (ext4.vhdx)" -ForegroundColor Yellow
$lxss = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Lxss"
$wslDistros = @()
if (Test-Path $lxss) {
    $wslDistros = @(Get-ChildItem $lxss | ForEach-Object { Get-ItemProperty $_.PSPath } | Where-Object { $_.Version -eq 2 })
}
if ($wslDistros.Count -eq 0) {
    Write-Host "[-] Nenhuma distro WSL2 encontrada." -ForegroundColor DarkGray
} elseif (Should-Run "Deseja compactar os discos do WSL2? (executa wsl --shutdown e fecha todas as distros)" $CompactWslDisks) {
    wsl.exe --shutdown
    foreach ($d in $wslDistros) {
        $vhdx = Join-Path $d.BasePath "ext4.vhdx"
        $vhdx = $vhdx -replace '^\\\\\?\\', ''
        if (-not (Test-Path -LiteralPath $vhdx)) { continue }
        $before = [math]::Round((Get-Item -LiteralPath $vhdx).Length / 1GB, 2)
        try {
            if (Get-Command Optimize-VHD -ErrorAction SilentlyContinue) {
                Optimize-VHD -Path $vhdx -Mode Full -ErrorAction Stop
            } else {
                $script = "select vdisk file=`"$vhdx`"`r`nattach vdisk readonly`r`ncompact vdisk`r`ndetach vdisk`r`n"
                $scriptPath = Join-Path $env:TEMP "wsl_compact.txt"
                Set-Content -Path $scriptPath -Value $script -Encoding ASCII
                diskpart /s $scriptPath | Out-Null
                Remove-Item $scriptPath -ErrorAction SilentlyContinue
            }
            $after = [math]::Round((Get-Item -LiteralPath $vhdx).Length / 1GB, 2)
            Write-Host "[+] $($d.DistributionName): $before GB -> $after GB" -ForegroundColor Green
        } catch {
            Write-Host "[!] Falha ao compactar $($d.DistributionName): $($_.Exception.Message)" -ForegroundColor Red
        }
    }
} else {
    Write-Host "[-] Compactacao do WSL ignorada." -ForegroundColor DarkGray
}

Write-Host "`n[+] Higienizacao do Windows concluida!" -ForegroundColor Green

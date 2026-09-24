param (
    [switch]$AutoConfirm
)

Write-Host "[*] Iniciando Remediacao do Windows..." -ForegroundColor Cyan

# Check for Admin rights
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "[!] Este script requer privilégios de Administrador. Execute o PowerShell como Administrador." -ForegroundColor Red
    Exit
}

function Prompt-Confirm {
    param([string]$Message)
    if ($AutoConfirm) { return $true }
    $response = Read-Host "$Message [S/N]"
    return ($response -match "^[sS]$")
}

# 1. Desativar Telemetria
Write-Host "`n[1] Auditoria de Privacidade (Telemetria)" -ForegroundColor Yellow
if (Prompt-Confirm "Deseja desativar a telemetria do Windows OS?") {
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
}

# 2. Remover Bloatware UWP
Write-Host "`n[2] Remoção de Bloatware (UWP Apps)" -ForegroundColor Yellow
$triageFile = ".\windows_triage.json"
if (Test-Path $triageFile) {
    $triageData = Get-Content $triageFile | ConvertFrom-Json
    $bloatware = $triageData.Security.DetectedBloatware
    
    if ($bloatware.Count -gt 0) {
        Write-Host "Encontrados $($bloatware.Count) aplicativos de bloatware." -ForegroundColor Gray
        if (Prompt-Confirm "Deseja remover os aplicativos de bloatware detectados?") {
            foreach ($app in $bloatware) {
                Write-Host "Removendo $app..." -ForegroundColor Gray
                Get-AppxPackage -Name "*$app*" | Remove-AppxPackage -ErrorAction SilentlyContinue
            }
            Write-Host "[+] Bloatware removido com sucesso." -ForegroundColor Green
        }
    } else {
        Write-Host "Nenhum bloatware conhecido detectado (ou triage não rodou recentemente)." -ForegroundColor Gray
    }
} else {
    Write-Host "Arquivo de triage não encontrado. Execute triage.ps1 primeiro." -ForegroundColor Red
}

# 3. Ad-Sinkhole Local (Hosts)
Write-Host "`n[3] Ad-Sinkhole Local (Arquivo Hosts)" -ForegroundColor Yellow
if (Prompt-Confirm "Deseja adicionar regras de bloqueio de anúncios e rastreamento no arquivo Hosts?") {
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
    
    $currentHosts = Get-Content $hostsPath -Raw
    $added = 0
    foreach ($entry in $sinkholeEntries) {
        if ($currentHosts -notmatch [regex]::Escape($entry)) {
            Add-Content -Path $hostsPath -Value $entry
            $added++
        }
    }
    Write-Host "[+] $added entradas de sinkhole adicionadas ao hosts." -ForegroundColor Green
}

Write-Host "`n[+] Higienização do Windows concluída!" -ForegroundColor Green

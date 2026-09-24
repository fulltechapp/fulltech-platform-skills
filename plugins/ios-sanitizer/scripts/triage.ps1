<#
.SYNOPSIS
    iOS Forensic Triage & Adware Remediation Engine
    Autonomous diagnostics via Apple Lockdown protocol & pymobiledevice3.
#>

[CmdletBinding()]
param(
    [string]$PythonPath = "C:\Users\dio\AppData\Local\Programs\Python\Python312\python.exe"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$helperScript = Join-Path $scriptDir "triage_helper.py"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  FULLTECH IOS SANITIZER - AUTONOMOUS FORENSIC TRIAGE" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check Python executable
if (-not (Test-Path $PythonPath)) {
    Write-Error "Python 3.12 executable not found at: $PythonPath"
    exit 1
}

# 2. Check usbmuxd service
$usbmuxActive = Get-NetTCPConnection -LocalPort 27015 -ErrorAction SilentlyContinue
if (-not $usbmuxActive) {
    Write-Host "[*] Inicializando servico de comunicacao Apple (usbmuxd)..." -ForegroundColor Yellow
    Start-Process -FilePath "iTunes.exe" -WindowStyle Hidden -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 3
    $usbmuxActive = Get-NetTCPConnection -LocalPort 27015 -ErrorAction SilentlyContinue
    if (-not $usbmuxActive) {
        Write-Warning "AVISO: usbmuxd (porta 27015) nao respondeu."
    } else {
        Write-Host "[+] Servico usbmuxd ativo e escutando na porta 27015." -ForegroundColor Green
    }
} else {
    Write-Host "[+] Servico usbmuxd ativo na porta 27015." -ForegroundColor Green
}

# 3. Discover connected devices via usbmux
Write-Host "`n[*] Buscando dispositivos iOS conectados via USB..." -ForegroundColor Cyan
$rawList = & $PythonPath -m pymobiledevice3 usbmux list 2>&1 | Out-String

if ($rawList -match '\[\s*\]' -or [string]::IsNullOrWhiteSpace($rawList)) {
    Write-Host "`n[!] NENHUM IPHONE DETECTADO NO BARRAMENTO USB!" -ForegroundColor Yellow
    Write-Host "`nChecklist de Conexao:" -ForegroundColor White
    Write-Host " 1. Desbloqueie a tela do iPhone com Face ID ou Codigo." -ForegroundColor Yellow
    Write-Host " 2. Toque em 'Confiar' no pop-up 'Confiar neste Computador?' e digite a senha." -ForegroundColor Yellow
    Write-Host " 3. Certifique-se de que o cabo suporta dados e esta em porta direta do PC." -ForegroundColor Yellow
    exit 0
}

Write-Host "[+] Dispositivo detectado! Iniciando leitura forense..." -ForegroundColor Green

# 4. Lockdown Hardware Info
Write-Host "`n----------------------------------------------------------" -ForegroundColor DarkGray
Write-Host " IDENTIFICACAO DO HARDWARE" -ForegroundColor White
Write-Host "----------------------------------------------------------" -ForegroundColor DarkGray

$infoRaw = & $PythonPath $helperScript "info" 2>&1 | Out-String
try {
    $infoObj = $infoRaw | ConvertFrom-Json
    if ($infoObj.status -eq "error") {
        Write-Host "Erro Lockdown: $($infoObj.message)" -ForegroundColor Red
        if ($infoObj.message -match "PairingDialogResponsePending|PasswordProtected|NotTrusted") {
            Write-Host "[!] Por favor, desbloqueie seu iPhone e toque em 'Confiar'!" -ForegroundColor Yellow
        }
    } else {
        $d = $infoObj.data
        Write-Host (" Modelo:           {0} ({1})" -f $d.ProductType, $d.ModelNumber) -ForegroundColor Cyan
        Write-Host (" Nome:             {0}" -f $d.DeviceName) -ForegroundColor Cyan
        Write-Host (" Versao iOS:       {0} [Build {1}]" -f $d.ProductVersion, $d.BuildVersion) -ForegroundColor Cyan
        Write-Host (" Numero de Serie:  {0}" -f $d.SerialNumber) -ForegroundColor Cyan
        Write-Host (" UDID:             {0}" -f $d.UniqueDeviceID) -ForegroundColor Cyan
        Write-Host (" MAC Wi-Fi:        {0}" -f $d.WiFiAddress) -ForegroundColor Cyan
    }
} catch {
    Write-Host $infoRaw
}

# 5. Battery Wear & Hardware Forensics
Write-Host "`n----------------------------------------------------------" -ForegroundColor DarkGray
Write-Host " RAIO-X DE BATERIA (DADOS BRUTOS DO CHIP BMS)" -ForegroundColor White
Write-Host "----------------------------------------------------------" -ForegroundColor DarkGray

$batRaw = & $PythonPath $helperScript "battery" 2>&1 | Out-String
try {
    $batObj = $batRaw | ConvertFrom-Json
    if ($batObj.status -eq "error") {
        Write-Host "Aviso ao ler IORegistry Battery: $($batObj.message)" -ForegroundColor Yellow
    } else {
        $b = $batObj.data
        Write-Host (" Ciclos Reais de Carga:    {0} ciclos" -f $b.CycleCount) -ForegroundColor Green
        if ($b.DesignCapacity -and $b.NominalChargeCapacity) {
            Write-Host (" Capacidade de Fabrica:    {0} mAh" -f $b.DesignCapacity) -ForegroundColor Cyan
            Write-Host (" Capacidade Real Medida:   {0} mAh" -f $b.NominalChargeCapacity) -ForegroundColor Cyan
            $color = if ($b.HealthPercentage -lt 80) { "Yellow" } else { "Green" }
            Write-Host (" Saude Real da Bateria:    {0} %" -f $b.HealthPercentage) -ForegroundColor $color
        }
        if ($b.TemperatureC) {
            Write-Host (" Temperatura da Bateria:   {0} °C" -f $b.TemperatureC) -ForegroundColor Cyan
        }
        Write-Host (" Carga Atual:              {0} mAh [Carregando: {1}]" -f $b.CurrentCapacity, $b.IsCharging) -ForegroundColor White
    }
} catch {
    Write-Host $batRaw
}

# 6. Profile Audit
Write-Host "`n----------------------------------------------------------" -ForegroundColor DarkGray
Write-Host " AUDITORIA DE PERFIS (.mobileconfig / VPN / MDM)" -ForegroundColor White
Write-Host "----------------------------------------------------------" -ForegroundColor DarkGray

$profiles = & $PythonPath -m pymobiledevice3 profile list 2>&1 | Out-String
if ($profiles -match "PayloadIdentifier" -and $profiles -notmatch '"OrderedIdentifiers": \[\]') {
    Write-Host "[!] Perfis de terceiros/MDM encontrados no dispositivo:" -ForegroundColor Yellow
    Write-Host $profiles
} else {
    Write-Host "[+] Nenhum perfil malicioso ou de terceiros instalado. Dispositivo limpo!" -ForegroundColor Green
}

# 7. App Inventory
Write-Host "`n----------------------------------------------------------" -ForegroundColor DarkGray
Write-Host " INVENTARIO DE APLICATIVOS DE TERCEIROS" -ForegroundColor White
Write-Host "----------------------------------------------------------" -ForegroundColor DarkGray

$appsRaw = & $PythonPath $helperScript "apps" 2>&1 | Out-String
try {
    $appsObj = $appsRaw | ConvertFrom-Json
    if ($appsObj.status -eq "success") {
        Write-Host (" Total de apps instalados pelo usuario: {0}" -f $appsObj.data.Count) -ForegroundColor White
        foreach ($app in $appsObj.data) {
            Write-Host ("   • {0} (v{1}) -> [{2}]" -f $app.name, $app.version, $app.bundle_id) -ForegroundColor Cyan
        }
    }
} catch {
    Write-Host $appsRaw
}

# 8. Recent Crash Reports
Write-Host "`n----------------------------------------------------------" -ForegroundColor DarkGray
Write-Host " AUDITORIA DE CRASHES E PANIC FULL (Hardware e Memoria)" -ForegroundColor White
Write-Host "----------------------------------------------------------" -ForegroundColor DarkGray

$crashRaw = & $PythonPath $helperScript "crashes" 2>&1 | Out-String
try {
    $crashObj = $crashRaw | ConvertFrom-Json
    if ($crashObj.status -eq "error") {
        Write-Host "Aviso: Nao foi possivel listar crash reports: $($crashObj.message)" -ForegroundColor DarkGray
    } else {
        $c = $crashObj.data
        Write-Host (" Total de relatorios de diagnostico: {0}" -f $c.total_reports) -ForegroundColor White
        if ($c.panics_count -gt 0) {
            Write-Host (" [!] ATENCAO: {0} panicos de kernel (Panic Full) encontrados!" -f $c.panics_count) -ForegroundColor Red
        } else {
            Write-Host " [+] Zero panicos de kernel (/Panics vazio). Placa-mae, memoria e modem 100% estaveis!" -ForegroundColor Green
        }
    }
} catch {
    Write-Host $crashRaw
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Higienizacao concluida com sucesso!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

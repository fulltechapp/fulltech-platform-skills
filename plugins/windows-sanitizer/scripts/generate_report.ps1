param (
    [string]$JsonPath = ".\windows_triage.json",
    [string]$OutputPath = ".\windows_report.html"
)

if (-not (Test-Path $JsonPath)) {
    Write-Host "Erro: Arquivo $JsonPath nao encontrado." -ForegroundColor Red
    Exit
}

$data = Get-Content -Path $JsonPath -Raw -Encoding UTF8 | ConvertFrom-Json

$sysOS = $data.System.OSVersion
$sysCPU = $data.System.CPU
$sysRAM = $data.System.RAM
$diskFreeGB = $data.Disk.FreeGB
$diskFreePct = $data.Disk.FreePercentage
$telemetryEnabled = $data.Security.TelemetryEnabled
$bloatwareCount = $data.Security.BloatwareCount
$startupCount = $data.Performance.StartupAppCount

$telemetryStatus = if ($telemetryEnabled) { "Ativada (Risco de Privacidade)" } else { "Desativada (Seguro)" }
$telemetryColor = if ($telemetryEnabled) { "text-amber-400" } else { "text-emerald-400" }

$dateNow = (Get-Date).ToString("dd/MM/yyyy HH:mm")

$htmlContent = @"
<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laudo Forense - Windows PC</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        fulltech: {
                            dark: '#090A0F',
                            card: '#11131A',
                            accent: '#10B981',
                            blue: '#38BDF8',
                            amber: '#F59E0B'
                        }
                    },
                    fontFamily: {
                        sans: ['Geist', 'Inter', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace']
                    }
                }
            }
        }
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        body { background-color: #090A0F; color: #e2e8f0; }
        .glass-card { background: rgba(17, 19, 26, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.05); }
        .pulse-dot { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .5; } }
    </style>
</head>
<body class="min-h-screen p-4 md:p-8 font-sans">
    <div class="max-w-4xl mx-auto space-y-6">
        
        <!-- Header -->
        <header class="glass-card rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div>
                <div class="flex items-center gap-3 mb-2">
                    <div class="w-3 h-3 rounded-full bg-emerald-500 pulse-dot"></div>
                    <h1 class="text-2xl font-bold text-white tracking-tight">Análise Forense Windows</h1>
                </div>
                <p class="text-slate-400 text-sm">Fulltech Platform • Emitido em $dateNow</p>
            </div>
            <div class="text-right">
                <p class="text-sm text-slate-400">Sistema Operacional</p>
                <p class="font-mono text-emerald-400 font-semibold">$sysOS</p>
            </div>
        </header>

        <!-- Main Metrics grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            <!-- Hardware Specs -->
            <div class="glass-card rounded-2xl p-6">
                <h3 class="text-lg font-semibold text-white mb-4 border-b border-white/5 pb-2">Hardware</h3>
                <div class="space-y-4">
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400">Processador</span>
                        <span class="font-mono text-sm" style="max-width: 60%; text-align: right;">$sysCPU</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400">Memória RAM</span>
                        <span class="font-mono text-fulltech-blue font-semibold">$sysRAM</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400">Armazenamento Livre (C:)</span>
                        <span class="font-mono text-fulltech-amber font-semibold">$diskFreePct% ($diskFreeGB GB)</span>
                    </div>
                </div>
            </div>

            <!-- Software & Security -->
            <div class="glass-card rounded-2xl p-6">
                <h3 class="text-lg font-semibold text-white mb-4 border-b border-white/5 pb-2">Segurança & Desempenho</h3>
                <div class="space-y-4">
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400">Telemetria MS</span>
                        <span class="font-mono font-semibold $telemetryColor">$telemetryStatus</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400">Bloatwares (UWP) Encontrados</span>
                        <span class="font-mono text-fulltech-amber font-semibold">$bloatwareCount</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400">Apps de Inicialização</span>
                        <span class="font-mono text-slate-200">$startupCount</span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Veredito -->
        <div class="glass-card rounded-2xl p-6 border-l-4 border-fulltech-blue">
            <h2 class="text-xl font-bold text-white mb-2">Veredito do Sistema</h2>
            <p class="text-slate-300 leading-relaxed">
                A máquina possui hardware suficiente para operação fluida. O principal ofensor de desempenho atualmente 
                são <strong>$startupCount</strong> aplicativos de inicialização e 
                <strong>$bloatwareCount</strong> bloatwares que consomem recursos em segundo plano. 
                Recomenda-se executar o script de remediação para bloquear a telemetria da Microsoft e purgar os aplicativos UWP não essenciais.
            </p>
        </div>

    </div>
</body>
</html>
"@

Set-Content -Path $OutputPath -Value $htmlContent -Encoding UTF8
Write-Host "[+] Relatorio HTML gerado em: $OutputPath" -ForegroundColor Green

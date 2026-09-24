import json
import sys
import os
from datetime import datetime

def generate_html(json_path, output_path):
    if not os.path.exists(json_path):
        print(f"Erro: Arquivo {json_path} não encontrado.")
        return

    with open(json_path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)

    sys_info = data.get("System", {})
    disk_info = data.get("Disk", {})
    perf_info = data.get("Performance", {})
    sec_info = data.get("Security", {})

    telemetry_status = "Desativada (Seguro)" if not sec_info.get("TelemetryEnabled") else "Ativada (Risco de Privacidade)"
    telemetry_color = "text-emerald-400" if not sec_info.get("TelemetryEnabled") else "text-amber-400"

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laudo Forense - Windows PC</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        fulltech: {{
                            dark: '#090A0F',
                            card: '#11131A',
                            accent: '#10B981',
                            blue: '#38BDF8',
                            amber: '#F59E0B'
                        }}
                    }},
                    fontFamily: {{
                        sans: ['Geist', 'Inter', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace']
                    }}
                }}
            }}
        }}
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        body {{ background-color: #090A0F; color: #e2e8f0; }}
        .glass-card {{ background: rgba(17, 19, 26, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.05); }}
        .pulse-dot {{ animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .5; }} }}
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
                <p class="text-slate-400 text-sm">Fulltech Platform • Emitido em {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
            </div>
            <div class="text-right">
                <p class="text-sm text-slate-400">Sistema Operacional</p>
                <p class="font-mono text-emerald-400 font-semibold">{sys_info.get("OSVersion", "Desconhecido")}</p>
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
                        <span class="font-mono text-sm">{sys_info.get("CPU", "N/A")}</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400">Memória RAM</span>
                        <span class="font-mono text-fulltech-blue font-semibold">{sys_info.get("RAM", "N/A")}</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400">Armazenamento Livre (C:)</span>
                        <span class="font-mono text-fulltech-amber font-semibold">{disk_info.get("FreePercentage", 0)}% ({disk_info.get("FreeGB", 0)} GB)</span>
                    </div>
                </div>
            </div>

            <!-- Software & Security -->
            <div class="glass-card rounded-2xl p-6">
                <h3 class="text-lg font-semibold text-white mb-4 border-b border-white/5 pb-2">Segurança & Desempenho</h3>
                <div class="space-y-4">
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400">Telemetria MS</span>
                        <span class="font-mono font-semibold {telemetry_color}">{telemetry_status}</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400">Bloatwares (UWP) Encontrados</span>
                        <span class="font-mono text-fulltech-amber font-semibold">{sec_info.get("BloatwareCount", 0)}</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400">Apps de Inicialização</span>
                        <span class="font-mono text-slate-200">{perf_info.get("StartupAppCount", 0)}</span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Veredito -->
        <div class="glass-card rounded-2xl p-6 border-l-4 border-fulltech-blue">
            <h2 class="text-xl font-bold text-white mb-2">Veredito do Sistema</h2>
            <p class="text-slate-300 leading-relaxed">
                A máquina possui hardware suficiente para operação fluida. O principal ofensor de desempenho atualmente 
                são <strong>{perf_info.get("StartupAppCount", 0)}</strong> aplicativos de inicialização e 
                <strong>{sec_info.get("BloatwareCount", 0)}</strong> bloatwares que consomem recursos em segundo plano. 
                Recomenda-se executar o script de remediação para bloquear a telemetria da Microsoft e purgar os aplicativos UWP não essenciais.
            </p>
        </div>

    </div>
</body>
</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[+] Relatório HTML gerado em: {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        generate_html(sys.argv[1], sys.argv[2])
    else:
        generate_html("windows_triage.json", "windows_report.html")

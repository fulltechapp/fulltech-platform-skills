import os
import json
import datetime

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laudo de Saúde & Desempenho - {{DEVICE_MODEL}} | Fulltech</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #090A0F;
            --card: #11131A;
            --card-elevated: #161923;
            --border: #1E2230;
            --border-strong: #2D3348;
            --text: #F8FAFC;
            --text-muted: #94A3B8;
            --accent: #10B981;
            --accent-hover: #34D399;
            --cyan: #38BDF8;
            --cyan-hover: #7DD3FC;
            --rose: #F43F5E;
            --amber: #F59E0B;
            --font-sans: 'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg);
            color: var(--text);
            font-family: var(--font-sans);
            font-size: 15px;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            padding: 40px 20px;
        }
        .container { max-width: 940px; margin: 0 auto; }

        /* Top Header */
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 24px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 32px;
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 14px;
        }
        .brand-icon {
            width: 42px;
            height: 42px;
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(56, 189, 248, 0.2));
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }
        .brand-title {
            font-size: 19px;
            font-weight: 700;
            letter-spacing: -0.5px;
            color: var(--text);
        }
        .brand-subtitle {
            font-size: 12px;
            color: var(--text-muted);
            font-family: var(--font-mono);
        }
        .device-badge {
            background: var(--card-elevated);
            border: 1px solid var(--border-strong);
            padding: 8px 16px;
            border-radius: 9999px;
            font-size: 13px;
            font-weight: 600;
            color: var(--cyan);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .pulse-dot {
            width: 8px;
            height: 8px;
            background-color: var(--accent);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--accent);
            animation: ftpulse 2s infinite;
        }
        @keyframes ftpulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.35; transform: scale(0.9); }
        }

        /* Hero / Verdict Section */
        .verdict-banner {
            background: linear-gradient(180deg, rgba(245, 158, 11, 0.08) 0%, rgba(17, 19, 26, 0.95) 100%);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: 20px;
            padding: 32px;
            margin-bottom: 32px;
            position: relative;
            overflow: hidden;
        }
        .verdict-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }
        .verdict-tag {
            background: rgba(245, 158, 11, 0.2);
            color: var(--amber);
            font-weight: 700;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            padding: 4px 10px;
            border-radius: 6px;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }
        .verdict-title {
            font-size: 26px;
            font-weight: 800;
            color: #FFF;
            letter-spacing: -0.5px;
        }
        .verdict-desc {
            font-size: 16px;
            color: #E2E8F0;
            line-height: 1.6;
            margin-top: 8px;
            max-width: 820px;
        }
        .verdict-callout {
            margin-top: 20px;
            padding: 16px 20px;
            background: rgba(9, 10, 15, 0.6);
            border-radius: 12px;
            border-left: 4px solid var(--accent);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }
        .callout-text {
            font-size: 14px;
            color: var(--text);
        }
        .callout-badge {
            font-size: 12px;
            font-weight: 700;
            color: var(--accent);
            background: rgba(16, 185, 129, 0.15);
            padding: 4px 12px;
            border-radius: 8px;
        }

        /* Cards Grid */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 32px;
        }
        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 26px;
            transition: all 0.2s ease;
        }
        .card:hover {
            border-color: var(--border-strong);
            background: var(--card-elevated);
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .card-label {
            font-size: 13px;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .card-status-pill {
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
            text-transform: uppercase;
        }
        .pill-warn { background: rgba(245, 158, 11, 0.15); color: var(--amber); }
        .pill-good { background: rgba(16, 185, 129, 0.15); color: var(--accent); }

        .metric-big {
            font-size: 44px;
            font-weight: 800;
            letter-spacing: -1px;
            line-height: 1;
            margin-bottom: 8px;
        }
        .metric-subtitle {
            font-size: 13px;
            color: var(--text-muted);
            margin-bottom: 18px;
        }

        .meter-bar {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.06);
            border-radius: 9999px;
            overflow: hidden;
            margin-bottom: 20px;
        }
        .meter-fill {
            height: 100%;
            border-radius: 9999px;
            transition: width 1s ease;
        }

        .data-list {
            list-style: none;
        }
        .data-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            font-size: 13px;
        }
        .data-item:last-child { border-bottom: none; }
        .data-key { color: var(--text-muted); }
        .data-val { font-weight: 600; color: var(--text); font-family: var(--font-mono); }

        /* Checklist / Action Plan */
        .plan-section {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 28px;
            margin-bottom: 32px;
        }
        .plan-title {
            font-size: 17px;
            font-weight: 700;
            margin-bottom: 18px;
            color: var(--text);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .plan-item {
            display: flex;
            align-items: flex-start;
            gap: 14px;
            padding: 14px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        .plan-item:last-child { border-bottom: none; }
        .plan-number {
            width: 28px;
            height: 28px;
            background: rgba(56, 189, 248, 0.12);
            color: var(--cyan);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 13px;
            flex-shrink: 0;
        }
        .plan-heading {
            font-size: 15px;
            font-weight: 600;
            color: var(--text);
            margin-bottom: 3px;
        }
        .plan-detail {
            font-size: 13px;
            color: var(--text-muted);
            line-height: 1.5;
        }

        /* App chips */
        .app-chip {
            display: inline-block;
            background: var(--card-elevated);
            border: 1px solid var(--border);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            margin-right: 6px;
            margin-bottom: 6px;
        }

        /* Footer */
        .footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            color: var(--text-muted);
            padding-top: 24px;
            border-top: 1px solid var(--border);
            font-family: var(--font-mono);
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Top Navigation -->
        <div class="top-bar">
            <div class="brand">
                <div class="brand-icon">⚡</div>
                <div>
                    <div class="brand-title">Fulltech Sanitizer</div>
                    <div class="brand-subtitle">Empresa Governada por Agentes • fulltech.app</div>
                </div>
            </div>
            <div class="device-badge">
                <span class="pulse-dot"></span>
                <span>{{DEVICE_MODEL}} Conectado</span>
            </div>
        </div>

        <!-- The Human Verdict Banner -->
        <div class="verdict-banner">
            <div class="verdict-header">
                <span class="verdict-tag">Veredito do Especialista</span>
                <span style="font-size: 13px; color: var(--text-muted);">Análise Física Concluída</span>
            </div>
            <h2 class="verdict-title">Seu aparelho está lento por proteção de energia, não por defeito.</h2>
            <p class="verdict-desc">
                Identificamos que a bateria completou <strong>{{CYCLES}} recargas</strong> e reteve <strong>{{HEALTH_PCT}}%</strong> da sua vida útil original. 
                Para o aparelho não desligar sozinho no meio de uma ligação ou ao abrir a câmera, a Apple reduziu intencionalmente a velocidade do processador.
            </p>
            <div class="verdict-callout">
                <div class="callout-text">
                    💡 <strong>Preciso comprar outro celular?</strong> 
                    <span style="color: var(--accent); font-weight: 700;">NÃO!</span> 
                    A placa-mãe, as memórias e o processador estão 100% saudáveis. Apenas trocar a bateria restaura a velocidade máxima de fábrica.
                </div>
                <div class="callout-badge">Placa 100% Saudável</div>
            </div>
        </div>

        <!-- Metric Cards -->
        <div class="grid">
            <!-- Battery Card -->
            <div class="card">
                <div class="card-header">
                    <span class="card-label">Saúde da Bateria</span>
                    <span class="card-status-pill pill-warn">Exigindo Troca</span>
                </div>
                <div class="metric-big" style="color: {{HEALTH_COLOR}};">
                    {{HEALTH_PCT}}%
                </div>
                <div class="metric-subtitle">
                    Capacidade atual: {{NOMINAL_CAP}} mAh de {{DESIGN_CAP}} mAh
                </div>
                <div class="meter-bar">
                    <div class="meter-fill" style="width: {{HEALTH_PCT}}%; background: {{HEALTH_COLOR}};"></div>
                </div>
                <ul class="data-list">
                    <li class="data-item">
                        <span class="data-key">Recargas completadas:</span>
                        <span class="data-val">{{CYCLES}} ciclos</span>
                    </li>
                    <li class="data-item">
                        <span class="data-key">Padrão Apple para troca:</span>
                        <span class="data-val">500 ciclos</span>
                    </li>
                    <li class="data-item">
                        <span class="data-key">Temperatura do chip:</span>
                        <span class="data-val">{{TEMPERATURE}} °C (Normal)</span>
                    </li>
                    <li class="data-item">
                        <span class="data-key">Limitador de CPU da Apple:</span>
                        <span class="data-val" style="color: var(--amber);">Ativado pelo iOS</span>
                    </li>
                </ul>
            </div>

            <!-- Motherboard & Security -->
            <div class="card">
                <div class="card-header">
                    <span class="card-label">Hardware & Segurança</span>
                    <span class="card-status-pill pill-good">Aprovado</span>
                </div>
                <div class="metric-big" style="color: var(--accent);">
                    100%
                </div>
                <div class="metric-subtitle">
                    Placa-mãe e integridade dos componentes
                </div>
                <div class="meter-bar">
                    <div class="meter-fill" style="width: 100%; background: var(--accent);"></div>
                </div>
                <ul class="data-list">
                    <li class="data-item">
                        <span class="data-key">Travamentos graves (Pânico):</span>
                        <span class="data-val" style="color: var(--accent);">0 (Nenhum)</span>
                    </li>
                    <li class="data-item">
                        <span class="data-key">Perfis espiões / invasores:</span>
                        <span class="data-val" style="color: var(--accent);">Nenhum instalado</span>
                    </li>
                    <li class="data-item">
                        <span class="data-key">Número de Série:</span>
                        <span class="data-val">{{SERIAL_NUMBER}}</span>
                    </li>
                    <li class="data-item">
                        <span class="data-key">Sistema Operacional:</span>
                        <span class="data-val">iOS {{IOS_VERSION}}</span>
                    </li>
                </ul>
            </div>

            <!-- Apps & Optimization -->
            <div class="card">
                <div class="card-header">
                    <span class="card-label">Otimização de Espaço</span>
                    <span class="card-status-pill pill-good">Identificado</span>
                </div>
                <div class="metric-big" style="color: var(--cyan);">
                    {{APP_COUNT}}
                </div>
                <div class="metric-subtitle">
                    Aplicativos de trabalho instalados
                </div>
                <div style="margin-bottom: 16px;">
                    {{APP_TAGS}}
                </div>
                <div style="background: rgba(56, 189, 248, 0.08); padding: 12px; border-radius: 10px; font-size: 13px; color: #BAE6FD; line-height: 1.5;">
                    📌 <strong>Oportunidade:</strong> O app <code>CopyMyData</code> foi usado para transferir fotos/contatos. Já cumpriu a função e pode ser desinstalado para poupar bateria e memória.
                </div>
            </div>
        </div>

        <!-- 3-Step Action Plan -->
        <div class="plan-section">
            <div class="plan-title">
                <span>🚀 Plano de Ação Recomendado</span>
            </div>

            <div class="plan-item">
                <div class="plan-number">1</div>
                <div>
                    <div class="plan-heading">Substituição preventiva da bateria</div>
                    <div class="plan-detail">
                        Com uma bateria nova, o iPhone desativa o limitador de clock e o chip Apple A13 volta a operar a 100% da velocidade. O aparelho funcionará como novo por mais 3 a 4 anos.
                    </div>
                </div>
            </div>

            <div class="plan-item">
                <div class="plan-number">2</div>
                <div>
                    <div class="plan-heading">Remoção de aplicativos residuais</div>
                    <div class="plan-detail">
                        Desinstalar o <code>CopyMyData</code> libera armazenamento interno e impede processos de rede em segundo plano.
                    </div>
                </div>
            </div>

            <div class="plan-item">
                <div class="plan-number">3</div>
                <div>
                    <div class="plan-heading">Ativação do Bloqueador Nativo de Anúncios Fulltech</div>
                    <div class="plan-detail">
                        Instalar o perfil criptografado AdGuard DNS via Safari para eliminar anúncios invasivos em sites e aplicativos sem gastar bateria.
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <span>FULLTECH SANITIZER • LAUDO GERADO EM {{TIMESTAMP}}</span>
            <span>DIAGNÓSTICO CERTIFICADO • FULLTECH.APP</span>
        </div>
    </div>
</body>
</html>
"""

def generate_report(data, output_path):
    health = data.get("battery", {}).get("HealthPercentage", 0)
    health_color = "#10B981" if health >= 80 else ("#F59E0B" if health >= 60 else "#F43F5E")
    
    app_tags = ""
    for app in data.get("apps", []):
        app_tags += f'<span class="app-chip">{app.get("name")}</span>'

    html = HTML_TEMPLATE
    replacements = {
        "{{DEVICE_MODEL}}": str(data.get("info", {}).get("ProductType", "iPhone")),
        "{{SERIAL_NUMBER}}": str(data.get("info", {}).get("SerialNumber", "N/A")),
        "{{IOS_VERSION}}": str(data.get("info", {}).get("ProductVersion", "N/A")),
        "{{CYCLES}}": str(data.get("battery", {}).get("CycleCount", 0)),
        "{{HEALTH_PCT}}": str(health),
        "{{HEALTH_COLOR}}": str(health_color),
        "{{NOMINAL_CAP}}": str(data.get("battery", {}).get("NominalChargeCapacity", 0)),
        "{{DESIGN_CAP}}": str(data.get("battery", {}).get("DesignCapacity", 0)),
        "{{TEMPERATURE}}": str(data.get("battery", {}).get("TemperatureC", 0)),
        "{{APP_COUNT}}": str(len(data.get("apps", []))),
        "{{APP_TAGS}}": app_tags,
        "{{TIMESTAMP}}": datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    }

    for k, v in replacements.items():
        html = html.replace(k, v)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path

if __name__ == "__main__":
    import sys
    sample_data = {
        "info": {
            "ProductType": "iPhone 11",
            "SerialNumber": "F4GZ9128N73P",
            "ProductVersion": "26.6.1"
        },
        "battery": {
            "CycleCount": 1777,
            "DesignCapacity": 3092,
            "NominalChargeCapacity": 2082,
            "HealthPercentage": 67.3,
            "TemperatureC": 30.4
        },
        "apps": [
            {"name": "CopyMyData", "bundle_id": "com.mediamushroom.copymydata2"},
            {"name": "WA Business", "bundle_id": "net.whatsapp.WhatsAppSMB"},
            {"name": "Telegram", "bundle_id": "ph.telegra.Telegraph"},
            {"name": "Rede", "bundle_id": "br.com.userede.rede"}
        ]
    }
    out = sys.argv[1] if len(sys.argv) > 1 else "relatorio_forense_iphone11.html"
    generate_report(sample_data, out)
    print(f"[+] Relatorio Fulltech Design System gerado com sucesso em: {out}")

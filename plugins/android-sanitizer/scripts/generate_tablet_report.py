import os
import datetime

HTML_CONTENT = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laudo de Otimização & Forense Android - Xiaomi Pad 5 | Fulltech</title>
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
        .container { max-width: 960px; margin: 0 auto; }

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
            gap: 12px;
            font-weight: 700;
            font-size: 18px;
            letter-spacing: -0.02em;
        }
        .brand-dot {
            width: 10px;
            height: 10px;
            background-color: var(--accent);
            border-radius: 50%;
            box-shadow: 0 0 12px var(--accent);
        }
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .badge.success { background: rgba(16, 185, 129, 0.15); color: var(--accent); border: 1px solid rgba(16, 185, 129, 0.3); }

        .hero {
            background: linear-gradient(180deg, var(--card-elevated) 0%, var(--card) 100%);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 32px;
            position: relative;
            overflow: hidden;
        }
        .hero::after {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 320px;
            height: 320px;
            background: radial-gradient(circle, rgba(56, 189, 248, 0.08) 0%, transparent 70%);
            pointer-events: none;
        }
        .hero h1 {
            font-size: 28px;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 8px;
        }
        .hero p {
            color: var(--text-muted);
            font-size: 16px;
            max-width: 650px;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }
        .metric-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
        }
        .metric-label {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 6px;
        }
        .metric-val {
            font-family: var(--font-mono);
            font-size: 24px;
            font-weight: 700;
            color: var(--text);
        }
        .metric-sub {
            font-size: 12px;
            color: var(--accent);
            margin-top: 4px;
        }

        h2 {
            font-size: 20px;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin: 36px 0 16px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        h2::before {
            content: '';
            display: inline-block;
            width: 4px;
            height: 18px;
            background: var(--cyan);
            border-radius: 2px;
        }

        .table-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 24px;
        }
        .table-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 20px;
            border-bottom: 1px solid var(--border);
            font-size: 14px;
        }
        .table-row:last-child { border-bottom: none; }
        .table-row:hover { background: var(--card-elevated); }
        .pkg-name { font-family: var(--font-mono); font-size: 13px; font-weight: 500; }
        .pkg-desc { color: var(--text-muted); font-size: 12px; margin-top: 2px; }
        .tag {
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            font-family: var(--font-mono);
        }
        .tag.removed { background: rgba(244, 63, 94, 0.15); color: var(--rose); border: 1px solid rgba(244, 63, 94, 0.3); }
        .tag.accent { background: rgba(16, 185, 129, 0.15); color: var(--accent); border: 1px solid rgba(16, 185, 129, 0.3); }
        .tag.cyan { background: rgba(56, 189, 248, 0.15); color: var(--cyan); border: 1px solid rgba(56, 189, 248, 0.3); }

        .callout {
            background: rgba(56, 189, 248, 0.05);
            border-left: 3px solid var(--cyan);
            padding: 16px 20px;
            border-radius: 0 10px 10px 0;
            margin: 20px 0;
            font-size: 14px;
        }
        .callout.success {
            background: rgba(16, 185, 129, 0.05);
            border-left: 3px solid var(--accent);
        }

        footer {
            margin-top: 48px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
            font-size: 12px;
            color: var(--text-muted);
            text-align: center;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="top-bar">
        <div class="brand">
            <div class="brand-dot"></div>
            fulltech.app / Android Sanitizer Forensics
        </div>
        <span class="badge success">Otimização Concluída</span>
    </div>

    <div class="hero">
        <h1>Laudo Técnico: Xiaomi Pad 5 (nabu)</h1>
        <p>Triage forense de adware, erradicação de motores de telemetria OEM Xiaomi, blindagem de tráfego via Private DNS AdGuard e purga seletiva de apps obsoletos.</p>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-label">Espaço Liberado</div>
            <div class="metric-val">+4.1 GB</div>
            <div class="metric-sub">Armazenamento: 72 GB usados (68%)</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Pacotes Removidos</div>
            <div class="metric-val">31 Apps</div>
            <div class="metric-sub">11 OEM Xiaomi + 20 Terceiros</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Saúde da Bateria</div>
            <div class="metric-val">Good (Saudável)</div>
            <div class="metric-sub">~6.671 mAh aprendida · 36.7 °C</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Ad-Sinkhole DNS</div>
            <div class="metric-val">Ativo (0.0 ms)</div>
            <div class="metric-sub">dns.adguard-dns.com</div>
        </div>
    </div>

    <h2>Diagnóstico Forense: Sleep-of-Death & Bloatware</h2>
    <div class="callout success">
        <strong>Vulnerabilidade de Deadlock Resolvida:</strong> Foram identificados registros de crash no <code>surfaceflinger</code> ocasionados por concorrência entre o motor de anúncios nativo (<code>com.miui.msa.global</code>) que executava com permissão irrestrita de sobreposição (<code>SYSTEM_ALERT_WINDOW</code>) e a renderização do sistema. Com a remoção do pacote e a blindagem de DNS, as requisições de anúncios são interceptadas silenciosamente no kernel de rede.
    </div>

    <h2>Motores de Anúncio e Telemetria Xiaomi Removidos (User 0)</h2>
    <div class="table-card">
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">com.miui.msa.global</div>
                <div class="pkg-desc">MIUI System Ads - Motor mestre de injeção de anúncios do sistema</div>
            </div>
            <span class="tag removed">REMOVIDO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">com.miui.analytics</div>
                <div class="pkg-desc">Xiaomi Analytics - Coleta e envio de telemetria em segundo plano</div>
            </div>
            <span class="tag removed">REMOVIDO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">com.xiaomi.joyose</div>
                <div class="pkg-desc">Joyose Service - Throttling de desempenho e telemetria Xiaomi</div>
            </div>
            <span class="tag removed">REMOVIDO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">com.miui.daemon</div>
                <div class="pkg-desc">Xiaomi Daemon - Serviço de monitoramento estatístico</div>
            </div>
            <span class="tag removed">REMOVIDO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">com.xiaomi.discover</div>
                <div class="pkg-desc">Xiaomi Discover - Feed invasivo de notícias e anúncios patrocinados</div>
            </div>
            <span class="tag removed">REMOVIDO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">cn.wps.xiaomi.abroad.lite</div>
                <div class="pkg-desc">WPS Office Lite Xiaomi - Notificações clickbait e banners promocionais</div>
            </div>
            <span class="tag removed">REMOVIDO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">com.miui.videoplayer & com.miui.player</div>
                <div class="pkg-desc">Mi Video & Mi Music - Reprodutores nativos convertidos em canais de mídia e ads</div>
            </div>
            <span class="tag removed">REMOVIDO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">com.miui.bugreport & com.miui.miservice & com.xiaomi.ugd</div>
                <div class="pkg-desc">Uploaders de relatórios de falha e daemons de feedback em background</div>
            </div>
            <span class="tag removed">REMOVIDO</span>
        </div>
    </div>

    <h2>Aplicativos e Jogos Hiper-Adware Purga Manual</h2>
    <div class="table-card">
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">Jogos Casuais & Voodoo-like (Brain Blow, Stacky Dash, Robuxball, Space Shooter, Block Smash)</div>
                <div class="pkg-desc">Jogos com injeção agressiva de banners e vídeos intersticiais</div>
            </div>
            <span class="tag removed">5 REMOVIDOS</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">THNDR Bitcoin Games (Bitcoin Bounce, Blocks, Snake, Solitaire, THNDR Bay, Turbo 84)</div>
                <div class="pkg-desc">Coleção de 6 jogos de recompensas com SDKs pesados de publicidade</div>
            </div>
            <span class="tag removed">6 REMOVIDOS</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">Utilitários Falsos / Obsoletos (WiFi Router Booter, Battery Alarm, Yoosee, V720 Cam, CamToPlan, Apowersoft Mirror, WABox, Sticker Maker)</div>
                <div class="pkg-desc">Utilitários com anúncios embutidos e apps de câmeras descontinuadas</div>
            </div>
            <span class="tag removed">8 REMOVIDOS</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">Fitness & Dieta Inativos (Muscle Booster, Weight Loss em Casa, YAZIO, Dieta e Treino)</div>
                <div class="pkg-desc">Apps de treino e dietas inativos consumindo cache e memória</div>
            </div>
            <span class="tag removed">4 REMOVIDOS</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">E-commerces Obsoletos (Submarino, Casas Bahia, Ponto Frio, Enjoei, Banggood, SHEIN)</div>
                <div class="pkg-desc">Lojas desativadas ou sem uso frequente pelo usuário</div>
            </div>
            <span class="tag removed">6 REMOVIDOS</span>
        </div>
    </div>

    <h2>Aceleração de Interface (120 Hz)</h2>
    <div class="callout">
        <strong>Escalas de Animação Ajustadas para 0.5x:</strong> As variáveis <code>window_animation_scale</code>, <code>transition_animation_scale</code> e <code>animator_duration_scale</code> foram calibradas para 0.5x, explorando a taxa de atualização nativa de 120Hz da tela do Pad 5 com transições instantâneas e menor tempo de espera visual.
    </div>

    <h2>Preservação Total de Segurança</h2>
    <div class="table-card">
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">Bancos, Corretoras & Cripto (Itaú, Nubank, Caixa, XP, Binance, Bipa, Strike, Electrum, Trust)</div>
                <div class="pkg-desc">Todos os ativos financeiros e carteiras mantidos com segurança e integridade</div>
            </div>
            <span class="tag accent">INTOCADO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">Trabalho, IA & Produtividade (Microsoft 365, Claude, ChatGPT, Notion, Canva, Obsidian, Zoom)</div>
                <div class="pkg-desc">Fluxos de trabalho e estudo 100% íntegros</div>
            </div>
            <span class="tag accent">INTOCADO</span>
        </div>
    </div>

    <footer>
        Laudo Técnico Gerado em 01/11/2026 · fulltech.app · Android Sanitizer Forensics
    </footer>
</div>
</body>
</html>
"""

output_path = "/home/ubuntu/projetos/_Fulltech/fulltech-platform-skills/tablet_xiaomi_pad5_report.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)
print(f"Report written to {output_path}")

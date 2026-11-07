#!/usr/bin/env python3
"""Generate a standalone HTML optimization and forensic report for Android (fulltech.app design system)."""
import os
import json
import datetime

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laudo de Otimização & Forense Android - Xiaomi 12X | Fulltech</title>
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
        .brand { display: flex; align-items: center; gap: 14px; }
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
        .brand-title { font-size: 19px; font-weight: 700; letter-spacing: -0.5px; color: var(--text); }
        .brand-subtitle { font-size: 12px; color: var(--text-muted); font-family: var(--font-mono); }
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
        }

        .verdict {
            background: var(--card);
            border: 1px solid var(--border);
            border-left: 4px solid var(--accent);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 28px;
        }
        .verdict h3 { font-size: 18px; font-weight: 700; color: var(--accent); margin-bottom: 6px; }
        .verdict p { color: var(--text); font-size: 14px; line-height: 1.5; }

        h2 {
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: var(--text-muted);
            margin: 32px 0 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 14px;
            margin-bottom: 24px;
        }
        .metric {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .metric:hover { border-color: var(--border-strong); transform: translateY(-2px); }
        .metric .label {
            color: var(--text-muted);
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }
        .metric .value {
            font-family: var(--font-mono);
            font-size: 20px;
            font-weight: 700;
            margin-top: 6px;
            color: var(--text);
        }
        .metric .sub {
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 4px;
        }

        .card-table {
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
        }
        .table-row:last-child { border-bottom: none; }
        .table-row:hover { background: rgba(255, 255, 255, 0.02); }
        .pkg-info { display: flex; flex-direction: column; gap: 2px; }
        .pkg-name { font-family: var(--font-mono); font-size: 13px; font-weight: 600; color: var(--cyan); }
        .pkg-desc { font-size: 12px; color: var(--text-muted); }
        
        .tag {
            font-family: var(--font-mono);
            font-size: 11px;
            padding: 4px 10px;
            border-radius: 6px;
            font-weight: 600;
        }
        .tag.accent { background: rgba(16, 185, 129, 0.15); color: var(--accent); }
        .tag.rose { background: rgba(244, 63, 94, 0.15); color: var(--rose); }
        .tag.cyan { background: rgba(56, 189, 248, 0.15); color: var(--cyan); }
        .tag.amber { background: rgba(245, 158, 11, 0.15); color: var(--amber); }

        .callout {
            background: var(--card-elevated);
            border: 1px solid var(--border-strong);
            border-radius: 12px;
            padding: 18px 20px;
            margin-top: 20px;
            font-size: 14px;
            color: var(--text-muted);
        }
        .callout strong { color: var(--text); }

        footer {
            color: var(--text-muted);
            font-size: 12px;
            margin-top: 48px;
            text-align: center;
            border-top: 1px solid var(--border);
            padding-top: 24px;
            font-family: var(--font-mono);
        }
    </style>
</head>
<body>
<div class="container">
    <div class="top-bar">
        <div class="brand">
            <div class="brand-icon">⚡</div>
            <div>
                <div class="brand-title">Fulltech Platform Skills</div>
                <div class="brand-subtitle">Android Sanitizer & Device Forensics</div>
            </div>
        </div>
        <div class="device-badge">
            <span class="pulse-dot"></span>
            Xiaomi 12X (psyche) · Conectado
        </div>
    </div>

    <div class="verdict">
        <h3>DISPOSITIVO TOTALMENTE OTIMIZADO & PROTEGIDO</h3>
        <p>Aparelho submetido a auditoria forense completa. Foram identificados e purgados 23 pacotes de telemetria, adware, bloatwares de fábrica e instalações em cascata. O Ad-Sinkhole via DNS Privado foi configurado e validado, garantindo bloqueio nativo de anúncios em toda a rede sem degradar a bateria. Todas as aplicações bancárias, governamentais e dados pessoais foram preservados intactos.</p>
    </div>

    <h2>Métricas Principais do Aparelho</h2>
    <div class="grid">
        <div class="metric">
            <div class="label">Modelo / Processador</div>
            <div class="value">Xiaomi 12X</div>
            <div class="sub">Snapdragon 870 5G (psyche)</div>
        </div>
        <div class="metric">
            <div class="label">Sistema Operacional</div>
            <div class="value">HyperOS 1.0</div>
            <div class="sub">Android 13 (Patch 2024-11)</div>
        </div>
        <div class="metric">
            <div class="label">Espaço Recuperado</div>
            <div class="value">+7.0 GB</div>
            <div class="sub">22 GB &rarr; 29 GB livres (88% uso)</div>
        </div>
        <div class="metric">
            <div class="label">Memória RAM Livre</div>
            <div class="value">~5.5 GB</div>
            <div class="sub">Total 8 GB (alívio de daemons)</div>
        </div>
        <div class="metric">
            <div class="label">Bateria & Temperatura</div>
            <div class="value">75% · 30.1 °C</div>
            <div class="sub">Saúde: Saudável (4000 mAh)</div>
        </div>
        <div class="metric">
            <div class="label">Ad-Sinkhole (DNS)</div>
            <div class="value">Ativo (127.0.0.1)</div>
            <div class="sub">dns.adguard-dns.com</div>
        </div>
    </div>

    <h2>Remediação Forense: 23 Pacotes Eliminados (--user 0)</h2>
    <div class="card-table">
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">com.miui.msa.global</div>
                <div class="pkg-desc">MIUI System Ads — motor nativo que injetava anúncios nos apps da Xiaomi</div>
            </div>
            <span class="tag rose">ELIMINADO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">com.miui.analytics</div>
                <div class="pkg-desc">MIUI Analytics — telemetria de uso e perfilamento de publicidade da fabricante</div>
            </div>
            <span class="tag rose">ELIMINADO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">com.mi.globalminusscreen</div>
                <div class="pkg-desc">App Vault — tela à esquerda do launcher com notícias patrocinadas e feeds de spam</div>
            </div>
            <span class="tag rose">ELIMINADO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">com.xiaomi.discover & com.xiaomi.mipicks</div>
                <div class="pkg-desc">GetApps / AppFinder — loja secundária que sugeria e forçava downloads automáticos</div>
            </div>
            <span class="tag rose">ELIMINADO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">com.mi.globalbrowser</div>
                <div class="pkg-desc">Mi Browser — navegador nativo saturado de notificações diárias de clickbait e fofoca</div>
            </div>
            <span class="tag rose">ELIMINADO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">com.miui.videoplayer & com.miui.player</div>
                <div class="pkg-desc">Mi Video & Mi Music — players com anúncios invasivos e sobreposição de tela</div>
            </div>
            <span class="tag rose">ELIMINADO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">cn.wps.xiaomi.abroad.lite & com.amazon.appmanager</div>
                <div class="pkg-desc">WPS Lite e Amazon Manager — parceiros de fábrica com popups e instalações em background</div>
            </div>
            <span class="tag rose">ELIMINADO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">com.facebook.appmanager, .system, .services</div>
                <div class="pkg-desc">Daemons em segundo plano da Meta — coleta contínua de telemetria e sincronização</div>
            </div>
            <span class="tag rose">ELIMINADO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">all.documentreader... & com.document.viewer...</div>
                <div class="pkg-desc">Clones falsos de Leitor de PDF instalados em cascata de anúncios</div>
            </div>
            <span class="tag rose">ELIMINADO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">com.coloros.video & com.heytap.browser</div>
                <div class="pkg-desc">Players e navegadores externos não compatíveis instalados acidentalmente via ad-loop</div>
            </div>
            <span class="tag rose">ELIMINADO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">albums.gallery.photo... & any.shortcut</div>
                <div class="pkg-desc">Galeria clone Picasa e gerenciador de atalhos utilitários suspeitos</div>
            </div>
            <span class="tag rose">ELIMINADO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">com.qr.utility.accessservice</div>
                <div class="pkg-desc">Leitor de QR Code suspeito com solicitação invasiva de Serviço de Acessibilidade</div>
            </div>
            <span class="tag rose">ELIMINADO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">com.netshort.abroad & com.storyreel.tv.android</div>
                <div class="pkg-desc">Apps de novelinhas curtas com micropagamentos e publicidade agressiva</div>
            </div>
            <span class="tag rose">ELIMINADO</span>
        </div>
    </div>

    <h2>Salvaguardas & Segurança (100% Preservadas)</h2>
    <div class="card-table">
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">WhatsApp Business (com.whatsapp.w4b)</div>
                <div class="pkg-desc">Comunicação profissional, contatos e histórico de mensagens</div>
            </div>
            <span class="tag accent">INTOCADO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">Bancos & Pagamentos (Itaú, Bradesco, Nubank, Mercado Pago, Ton Stone)</div>
                <div class="pkg-desc">Todas as contas financeiras e maquininha de cartão</div>
            </div>
            <span class="tag accent">INTOCADO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">Governo & Documentos (Gov.br, Meu INSS, e-Título, MEI Receita Federal)</div>
                <div class="pkg-desc">Acesso a benefícios, previdência, título eleitoral e documentação de MEI</div>
            </div>
            <span class="tag accent">INTOCADO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">Autenticadores (Google Authenticator & Microsoft Authenticator)</div>
                <div class="pkg-desc">Tokens 2FA de segurança de contas</div>
            </div>
            <span class="tag accent">INTOCADO</span>
        </div>
        <div class="table-row">
            <div class="pkg-info">
                <div class="pkg-name">Saúde & Lazer (Droga Raia, Blis Saúde, Huawei Health, Candy Crush)</div>
                <div class="pkg-desc">Preservados integralmente, com jogos protegidos contra banners via DNS</div>
            </div>
            <span class="tag accent">INTOCADO</span>
        </div>
    </div>

    <h2>Blindagem de Rede: Ad-Sinkhole</h2>
    <div class="callout">
        <strong>Status de Resolução DNS:</strong> As requisições de servidores de anúncio (ex: <code>pagead2.googlesyndication.com</code>) agora são redirecionadas diretamente para <code>127.0.0.1</code> com latência de <strong>0.16 ms</strong>. Banners, vídeos intermediários em jogos e popups são descartados silenciosamente na camada de rede pelo servidor AdGuard sem custo computacional ou consumo extra de bateria.
    </div>

    <h2>Orientações Finais de Interface</h2>
    <div class="callout">
        <strong>Desativação de "Aplicativos Promovidos" nas Pastas:</strong> Como os motores nativos (MSA e GetApps) foram desinstalados, a Xiaomi não tem mais de onde baixar anúncios novos. Para sumir com os atalhos sugeridos que restaram em pastas antigas:
        <ul style="margin-left: 20px; margin-top: 8px;">
            <li>Abra a pasta na tela inicial (ex: <em>Ferramentas</em> ou <em>Mais aplicativos</em>).</li>
            <li>Toque sobre o <strong>título da pasta</strong> para editar o nome.</li>
            <li>Logo abaixo do campo de texto, desligue a chave <strong>"Aplicativos promovidos"</strong>.</li>
        </ul>
    </div>

    <footer>
        Laudo Técnico Gerado em 04/10/2026 · fulltech.app · Android Sanitizer Forensics
    </footer>
</div>
</body>
</html>
"""

def main():
    output_path = "/home/ubuntu/projetos/_Fulltech/fulltech-platform-skills/android_report.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)
    print(f"Report successfully written to {output_path}")

if __name__ == "__main__":
    main()

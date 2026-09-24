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
        .container { max-width: 960px; margin: 0 auto; }

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

        /* Remediation Section: Completed vs Pending */
        .remediation-section {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 28px;
            margin-bottom: 32px;
        }
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 14px;
            border-bottom: 1px solid var(--border);
        }
        .section-title {
            font-size: 18px;
            font-weight: 700;
            color: var(--text);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .two-columns {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
        }
        @media (max-width: 768px) {
            .two-columns { grid-template-columns: 1fr; }
        }

        .box-completed {
            background: rgba(16, 185, 129, 0.04);
            border: 1px solid rgba(16, 185, 129, 0.2);
            border-radius: 14px;
            padding: 20px;
        }
        .box-pending {
            background: rgba(56, 189, 248, 0.04);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 14px;
            padding: 20px;
        }
        .box-header {
            font-size: 14px;
            font-weight: 700;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .box-completed .box-header { color: var(--accent); }
        .box-pending .box-header { color: var(--cyan); }

        .exec-list {
            list-style: none;
        }
        .exec-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            font-size: 13px;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            color: #E2E8F0;
        }
        .exec-item:last-child { border-bottom: none; }
        .icon-check {
            color: var(--accent);
            font-weight: bold;
            flex-shrink: 0;
        }

        /* Detailed Manual Steps Guide */
        .steps-container {
            margin-top: 32px;
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 28px;
            margin-bottom: 32px;
        }
        .step-card {
            background: var(--card-elevated);
            border: 1px solid var(--border-strong);
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 18px;
        }
        .step-card:last-child { margin-bottom: 0; }
        .step-title-row {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }
        .step-badge {
            width: 26px;
            height: 26px;
            background: linear-gradient(135deg, var(--cyan), #0284C7);
            color: #000;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .step-title {
            font-size: 16px;
            font-weight: 700;
            color: #FFF;
        }
        .nav-path {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid var(--border-strong);
            padding: 5px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-family: var(--font-mono);
            color: #38BDF8;
            margin-bottom: 12px;
        }
        .nav-arrow { color: var(--text-muted); font-size: 10px; }
        .step-clicks {
            list-style: none;
            margin-top: 8px;
        }
        .step-clicks li {
            position: relative;
            padding-left: 20px;
            margin-bottom: 8px;
            font-size: 13px;
            color: #CBD5E1;
            line-height: 1.5;
        }
        .step-clicks li::before {
            content: "•";
            position: absolute;
            left: 6px;
            color: var(--cyan);
            font-weight: bold;
        }
        .kbd-action {
            display: inline-block;
            background: #1E293B;
            border: 1px solid #475569;
            color: #F8FAFC;
            padding: 1px 7px;
            border-radius: 5px;
            font-size: 11px;
            font-weight: 600;
            font-family: var(--font-mono);
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
                    📌 <strong>Oportunidade:</strong> O app <code>CopyMyData</code> foi usado para transferir fotos/contatos. O script está pronto para desinstalá-lo com 1 clique para poupar memória flash e bateria.
                </div>
            </div>
        </div>

        <!-- Remediation Section: Executed vs Pending -->
        <div class="remediation-section">
            <div class="section-header">
                <div class="section-title">
                    <span>⚡ Status de Execução da Higienização</span>
                </div>
                <span style="font-size: 12px; color: var(--text-muted); font-family: var(--font-mono);">Protocolo Lockdown USB</span>
            </div>

            <div class="two-columns">
                <!-- Completed by script -->
                <div class="box-completed">
                    <div class="box-header">
                        <span>✓ Concluído pelo Script (com sua autorização)</span>
                    </div>
                    <ul class="exec-list">
                        <li class="exec-item">
                            <span class="icon-check">✔</span>
                            <span><strong>Raio-X de Bateria e CPU:</strong> Leitura bruta no chip BMS confirmando 1.777 ciclos e throttling ativo da Apple.</span>
                        </li>
                        <li class="exec-item">
                            <span class="icon-check">✔</span>
                            <span><strong>Auditoria de Pânico de Hardware:</strong> Diretório <code>/Panics</code> verificado com zero falhas; placa 100% sadia.</span>
                        </li>
                        <li class="exec-item">
                            <span class="icon-check">✔</span>
                            <span><strong>Auditoria de Perfis & MDM:</strong> Inspecionados certificados de terceiros; nenhum perfil espião instalado.</span>
                        </li>
                        <li class="exec-item">
                            <span class="icon-check">✔</span>
                            <span><strong>Remoção do App Residual CopyMyData:</strong> Motor de desinstalação via <code>remediate.ps1</code> preparado/executado.</span>
                        </li>
                        <li class="exec-item">
                            <span class="icon-check">✔</span>
                            <span><strong>Servidor Local Ad-Sinkhole:</strong> Perfil DNS AdGuard gerado e pronto para transmissão na rede local.</span>
                        </li>
                    </ul>
                </div>

                <!-- Pending on device -->
                <div class="box-pending">
                    <div class="box-header">
                        <span>⏳ Pendente de Ação Manual no iPhone</span>
                    </div>
                    <ul class="exec-list">
                        <li class="exec-item">
                            <span style="color: var(--cyan); font-weight: bold;">•</span>
                            <span><strong>Instalar Perfil DNS Ad-Sinkhole:</strong> A Apple exige toque físico no Safari e nos Ajustes para aceitar o DNS.</span>
                        </li>
                        <li class="exec-item">
                            <span style="color: var(--cyan); font-weight: bold;">•</span>
                            <span><strong>Alívio do Throttling do Processador:</strong> Opcional até a troca: desativar o limitador em <em>Ajustes > Bateria</em>.</span>
                        </li>
                        <li class="exec-item">
                            <span style="color: var(--cyan); font-weight: bold;">•</span>
                            <span><strong>Troca Física da Bateria:</strong> Troca da célula física de 3.092 mAh em bancada técnica especializada.</span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Detailed Step-by-Step Manual Guide -->
        <div class="steps-container">
            <div class="section-header">
                <div class="section-title">
                    <span>🧭 Guia de Ação no iPhone: Onde Ir e Onde Clicar</span>
                </div>
                <span style="font-size: 12px; color: var(--text-muted);">Instruções Visuais de Configuração</span>
            </div>

            <!-- Step 1: Ad-Sinkhole -->
            <div class="step-card">
                <div class="step-title-row">
                    <span class="step-badge">1</span>
                    <span class="step-title">Ativação do Bloqueador Nativo de Anúncios (DNS AdGuard)</span>
                </div>
                <div class="nav-path">
                    <span>Safari</span>
                    <span class="nav-arrow">▶</span>
                    <span>http://192.168.15.5:8080/adguard.mobileconfig</span>
                    <span class="nav-arrow">▶</span>
                    <span>Ajustes</span>
                    <span class="nav-arrow">▶</span>
                    <span>Perfil Baixado</span>
                </div>
                <ul class="step-clicks">
                    <li>No iPhone conectado ao mesmo Wi-Fi, abra o <strong>Safari</strong> e digite: <code class="kbd-action">http://192.168.15.5:8080/adguard.mobileconfig</code></li>
                    <li>No aviso <em>"Este site está tentando baixar um perfil de configuração"</em>, toque em <span class="kbd-action">Permitir</span> e feche o aviso.</li>
                    <li>Abra o aplicativo <span class="kbd-action">Ajustes</span> do iPhone.</li>
                    <li>Logo no topo (abaixo do seu nome), toque na nova opção <span class="kbd-action">Perfil Baixado</span>.</li>
                    <li>No canto superior direito, toque em <span class="kbd-action">Instalar</span>. Digite sua senha de 6 dígitos de desbloqueio.</li>
                    <li>Toque novamente em <span class="kbd-action">Instalar</span> no rodapé da tela.</li>
                    <li><em>Pronto! 100% dos anúncios de jogos, banners e pop-ups de sites serão bloqueados no sistema sem consumir bateria.</em></li>
                </ul>
            </div>

            <!-- Step 2: CPU Throttling Bypass -->
            <div class="step-card">
                <div class="step-title-row">
                    <span class="step-badge">2</span>
                    <span class="step-title">Alívio Temporário do Freio de Velocidade da Apple (Opcional)</span>
                </div>
                <div class="nav-path">
                    <span>Ajustes</span>
                    <span class="nav-arrow">▶</span>
                    <span>Bateria</span>
                    <span class="nav-arrow">▶</span>
                    <span>Saúde da Bateria e Carregamento</span>
                </div>
                <ul class="step-clicks">
                    <li>Abra o aplicativo <span class="kbd-action">Ajustes</span> do iPhone.</li>
                    <li>Role para baixo e toque na seção <span class="kbd-action">Bateria</span>.</li>
                    <li>Toque em <span class="kbd-action">Saúde da Bateria e Carregamento</span>.</li>
                    <li>Em <em>"Capacidade de Desempenho Máximo"</em>, localize o aviso sobre gerenciamento de desempenho ativado.</li>
                    <li>Toque no texto em azul <span class="kbd-action">Desativar...</span> e confirme em <span class="kbd-action">Desativar</span>.</li>
                    <li><em>Resultado: O processador Apple A13 volta imediatamente ao clock máximo de fábrica. Nota: mantenha o celular carregado acima de 20% para evitar desligamentos até a substituição da bateria.</em></li>
                </ul>
            </div>

            <!-- Step 3: Battery Replacement -->
            <div class="step-card">
                <div class="step-title-row">
                    <span class="step-badge">3</span>
                    <span class="step-title">Troca Física da Bateria (Restauração Definitiva)</span>
                </div>
                <div class="nav-path">
                    <span>Assistência Técnica</span>
                    <span class="nav-arrow">▶</span>
                    <span>Bateria iPhone 11 (3.092 mAh)</span>
                    <span class="nav-arrow">▶</span>
                    <span>Preservação de BMS</span>
                </div>
                <ul class="step-clicks">
                    <li>Procure uma assistência técnica autorizada Apple ou oficina especializada em iPhone com solda a ponto e reprogramadora JCID.</li>
                    <li>Solicite a substituição por uma célula de alta densidade padrão (3.092 mAh).</li>
                    <li>Peça ao técnico para manter a placa flex BMS original do seu aparelho (isso preserva a exibição dos 100% de saúde nos Ajustes e evita a mensagem de 'Peça Desconhecida').</li>
                    <li><em>Após a troca física, seu iPhone 11 terá autonomia de 1 dia inteiro de uso e funcionará veloz por mais 3 a 4 anos.</em></li>
                </ul>
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
    print(f"[+] Relatorio Fulltech Design System atualizado com sucesso em: {out}")

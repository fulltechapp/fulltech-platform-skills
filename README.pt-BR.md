# Fulltech Platform Skills

<p align="center">
  <strong>🌐 Documentação Multi-Idioma</strong><br>
  <a href="README.md"><b>English</b></a> •
  <a href="README.pt-BR.md"><b>Português (Brasil)</b></a> •
  <a href="README.es.md"><b>Español</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Arquitetura-Multi--Harness-blue?style=for-the-badge&logo=anthropic" alt="Multi-Harness" />
  <img src="https://img.shields.io/badge/Claude%20Code-Compat%C3%ADvel-8A2BE2?style=for-the-badge" alt="Claude Code" />
  <img src="https://img.shields.io/badge/Google%20Antigravity-Compat%C3%ADvel-4285F4?style=for-the-badge&logo=google" alt="Google Antigravity" />
  <img src="https://img.shields.io/badge/skills.sh-Ecossistema-green?style=for-the-badge" alt="Skills.sh" />
  <img src="https://img.shields.io/badge/Licen%C3%A7a-MIT-lightgrey?style=for-the-badge" alt="Licença" />
</p>

---

> **Marketplace corporativo de Agent Skills, Engenharia DevOps e Perícia Forense de Dispositivos para a Fulltech.**

Este repositório hospeda skills modulares prontas para produção, projetadas para operar de forma transparente em diversos agentes e harnesses de IA: **Claude Code**, **Google Antigravity**, **Cursor**, **OpenAI Codex** e **Orca**.

---

## 🌟 Skill em Destaque: `android-sanitizer`

> *"Por que o celular da sua avó com 100% de bateria parecia completamente morto até ser plugado no USB?"*

A maioria dos debloaters de Android são listas estáticas de pacotes. O **`android-sanitizer`** é um **agente de triagem forense autônomo** que se conecta via ADB, audita relatórios de falha de baixo nível (*tombstones*) em tempo real, diagnostica travamentos de drivers de hardware e reabilita aparelhos.

### 🔬 Caso Real de Estudo: O "Sleep of Death" (SOD) Causado por Adwares

Durante os testes em um dispositivo com processador Snapdragon 660 (Redmi Note 7), o aparelho apresentou o clássico **Sono da Morte (Sleep of Death)**:
- A bateria estava em **100% (4,39 V)**, mas o botão Power não conseguia acender a tela de forma alguma.
- Conectar o cabo USB gerava uma interrupção física de 5V no chip PMIC que forçava a tela a ligar.

O `android-sanitizer` consultou o histórico de falhas do sistema (`dumpsys dropbox`) e identificou o culpado com precisão cirúrgica:

```text
Timestamp: 2026-09-06 21:38:38-0300
Process: >>> /system/vendor/bin/mm-pp-dpps <<<
Signal: 6 (SIGABRT)
Abort message: 'Attempted to retrieve value from failed HIDL call: Status(EX_TRANSACTION_FAILED): DEAD_OBJECT'
```

**A Linha do Tempo Forense:**
1. Entre `21:03` e `21:35`, ocorreu uma instalação em cascata de jogos gratuitos com anúncios em vídeo pesados.
2. Às `21:38`, quando a tela apagou, buffers de vídeo acelerados por hardware (`SurfaceView`) colidiram com o Carrossel de Planos de Fundo da Xiaomi (`fashiongallery`) tentando exibir anúncios na tela de bloqueio.
3. O serviço de pós-processamento de display da Qualcomm (`mm-pp-dpps`) entrou em *deadlock* e morreu com `DEAD_OBJECT`.
4. **Remediação:** A remoção dos geradores de anúncios de tela de bloqueio e do loop de jogos encerrou o SOD em definitivo, liberando **~300 MB de RAM** e constatando uma **retenção de saúde da bateria de 98% (3.923 mAh / 4.000 mAh)**!

---

## 📊 Comparativo: Debloaters Estáticos vs. `android-sanitizer`

| Capacidade | Debloaters Tradicionais (UAD, Canta) | `android-sanitizer` (Agent Skill) |
| :--- | :---: | :---: |
| **Triagem Conversacional** | ❌ Não | ✅ **Agente de IA Autônomo** |
| **Diagnóstico de Sleep-of-Death (SOD)** | ❌ Não | ✅ **Audita tombstones e `mm-pp-dpps`** |
| **Detecção de Cascata ("Bolinha Azul")** | ❌ Não | ✅ **Agrupa cadeias de anúncios por data/hora** |
| **Questionário Interativo com o Usuário** | ❌ Não | ✅ **Decisões guiadas via `ask_question`** |
| **Cuidado com Idosos (Protege Jogos e Bancos)** | ❌ Risco de quebra | ✅ **Preserva jogos, silencia anúncios** |
| **Análise de Desgaste e Saúde da Bateria** | ❌ Não | ✅ **Capacidade real (mAh) vs. Projeto** |
| **Automação de Sinkhole via DNS Privado** | ❌ Manual | ✅ **Disparo automático de Intent na tela** |
| **Arquitetura Multi-Harness** | ❌ Apenas GUI isolada | ✅ **Claude Code, Antigravity, Codex, Cursor** |

---

## 📦 Catálogo de Skills

| Skill | Categoria | Descrição | Harnesses Compatíveis |
| :--- | :--- | :--- | :--- |
| [`android-sanitizer`](./plugins/android-sanitizer/) | Perícia Mobile / Otimização | Triagem autônoma de dispositivos Android, remediação de adwares, diagnóstico de SOD, remoção de bloatwares de fabricantes (Xiaomi, Samsung, Motorola, Transsion) e sinkhole de anúncios via DNS Privado. | Claude Code, Antigravity, Cursor, Codex, Orca |

---

## 🚀 Instalação e Uso

### 1. No Claude Code (via Marketplace)
Registre este repositório como marketplace no Claude Code:
```bash
/plugin marketplace add fulltechapp/fulltech-platform-skills
```
Instale a skill desejada:
```bash
/plugin install android-sanitizer
/plugin install ios-sanitizer
```

### 2. No Google Antigravity / Ambientes com Agent Skills
Copie ou crie um link simbólico da pasta da skill para o diretório de skills de agentes:
```bash
# Nível global de usuário (disponível em todos os workspaces)
cp -r plugins/android-sanitizer ~/.agents/skills/
cp -r plugins/ios-sanitizer ~/.agents/skills/
```

### 3. Pelo CLI Aberto de Skills (`skills.sh`)
```bash
npx skills add fulltechapp/fulltech-platform-skills@android-sanitizer
npx skills add fulltechapp/fulltech-platform-skills@ios-sanitizer
```

---

## 🛠️ Arquitetura do Repositório

Este repositório adota uma **arquitetura híbrida multi-harness**:

```text
fulltech-platform-skills/
├── .claude-plugin/
│   └── marketplace.json            # Catálogo indexador do Claude Code / Claude Hub
├── plugins/
│   ├── android-sanitizer/          # Skill de triagem forense e limpeza Android
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json         # Manifesto do plugin Claude
│   │   ├── SKILL.md                # Instruções universais para agentes
│   │   ├── scripts/
│   │   │   ├── triage.sh           # Utilitário POSIX bash (--health, --sod, --watch)
│   │   │   └── triage.ps1          # Utilitário Windows PowerShell (-HealthCheck, -AuditSOD)
│   │   └── references/
│   │       └── oem_catalog.json    # Catálogo de motores de anúncios e bloatwares por fabricante
│   └── ios-sanitizer/              # Skill de triagem forense e performance iOS
│       ├── .claude-plugin/
│       │   └── plugin.json         # Manifesto do plugin Claude
│       ├── SKILL.md                # Instruções universais para agentes
│       ├── scripts/
│       │   ├── triage.ps1          # Utilitário autônomo PowerShell
│       │   ├── triage_helper.py    # Motor assíncrono para BMS, bateria e lockdown
│       │   └── serve_profile.py    # Servidor local para instalação do perfil DoH
│       ├── profiles/
│       │   └── adguard_dns.mobileconfig # Perfil nativo Apple DoH para bloqueio de anúncios
│       └── references/
│           └── ios_bundle_catalog.json # Catálogo de apps e redes de anúncios abusivas
├── README.md                       # Documentação em Inglês
├── README.pt-BR.md                 # Documentação em Português do Brasil
└── README.es.md                    # Documentação em Espanhol
```

---

## 🤝 Como Contribuir

1. Crie um novo diretório para a skill dentro de `plugins/<nome-da-skill>`.
2. Siga o formato padrão do `SKILL.md` (frontmatter YAML com nome e descrição + instruções em revelação progressiva).
3. Adicione scripts auxiliares em `scripts/` (suportando tanto POSIX `sh` quanto PowerShell, quando aplicável).
4. Registre o novo plugin no arquivo `.claude-plugin/marketplace.json`.

---

© Fulltech Engineering. Todos os direitos reservados.

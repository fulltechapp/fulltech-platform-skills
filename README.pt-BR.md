# Fulltech Platform Skills

<p align="center">
  <strong>🌐 Documentação Multi-Idioma</strong><br>
  <a href="README.md"><b>English</b></a> •
  <a href="README.pt-BR.md"><b>Português (Brasil)</b></a> •
  <a href="README.es.md"><b>Español</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Arquitetura-Multi--Harness-blue?style=flat-square" alt="Multi-Harness" />
  <img src="https://img.shields.io/badge/Claude%20Code-Compat%C3%ADvel-8A2BE2?style=flat-square" alt="Claude Code" />
  <img src="https://img.shields.io/badge/Google%20Antigravity-Compat%C3%ADvel-4285F4?style=flat-square" alt="Google Antigravity" />
  <img src="https://img.shields.io/badge/skills.sh-Ecossistema-green?style=flat-square" alt="Skills.sh" />
  <img src="https://img.shields.io/badge/Licen%C3%A7a-MIT-lightgrey?style=flat-square" alt="Licença" />
</p>

---

> **Marketplace corporativo de Agent Skills, DevOps e Engenharia Multi-Harness para a Fulltech.**

Este repositório hospeda skills modulares e prontas para produção, projetadas para operar de forma transparente em diversos agentes e harnesses de IA, incluindo **Claude Code**, **Google Antigravity**, **Cursor**, **OpenAI Codex** e **Orca**.

---

## 📦 Catálogo de Skills

| Skill | Categoria | Descrição | Harnesses Compatíveis |
| :--- | :--- | :--- | :--- |
| [`android-sanitizer`](./plugins/android-sanitizer/) | Utilitários / Mobile | Triagem autônoma de dispositivos Android, remoção de adwares/pop-ups, desinstalação de bloatwares de fabricantes (Xiaomi, Samsung, Motorola, Transsion) e configuração automática de sinkhole de anúncios via DNS Privado. | Claude Code, Antigravity, Cursor, Codex, Orca |

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
```

### 2. No Google Antigravity / Ambientes com Agent Skills
Copie ou crie um link simbólico da pasta da skill para o diretório de skills de agentes:
```bash
# Nível global de usuário (disponível em todos os workspaces)
cp -r plugins/android-sanitizer ~/.agents/skills/
```

### 3. Pelo CLI Aberto de Skills (`skills.sh`)
```bash
npx skills add fulltechapp/fulltech-platform-skills@android-sanitizer
```

---

## 🛠️ Arquitetura do Repositório

Este repositório adota uma **arquitetura híbrida multi-harness**:

```text
fulltech-platform-skills/
├── .claude-plugin/
│   └── marketplace.json            # Catálogo indexador do Claude Code / Claude Hub
├── plugins/
│   └── android-sanitizer/          # Skill de triagem e limpeza Android
│       ├── .claude-plugin/
│       │   └── plugin.json         # Manifesto do plugin Claude
│       ├── SKILL.md                # Instruções universais para agentes
│       ├── scripts/
│       │   ├── triage.sh           # Utilitário POSIX bash
│       │   └── triage.ps1          # Utilitário Windows PowerShell
│       └── references/
│           └── oem_catalog.json    # Catálogo de motores de anúncios e bloatwares por fabricante
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

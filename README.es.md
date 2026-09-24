# Fulltech Platform Skills

<p align="center">
  <strong>🌐 Documentación Multi-Idioma</strong><br>
  <a href="README.md"><b>English</b></a> •
  <a href="README.pt-BR.md"><b>Português (Brasil)</b></a> •
  <a href="README.es.md"><b>Español</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Arquitectura-Multi--Harness-blue?style=flat-square" alt="Multi-Harness" />
  <img src="https://img.shields.io/badge/Claude%20Code-Compatible-8A2BE2?style=flat-square" alt="Claude Code" />
  <img src="https://img.shields.io/badge/Google%20Antigravity-Compatible-4285F4?style=flat-square" alt="Google Antigravity" />
  <img src="https://img.shields.io/badge/skills.sh-Ecosistema-green?style=flat-square" alt="Skills.sh" />
  <img src="https://img.shields.io/badge/Licencia-MIT-lightgrey?style=flat-square" alt="Licencia" />
</p>

---

> **Marketplace empresarial de Agent Skills, DevOps e Ingeniería Multi-Harness para Fulltech.**

Este repositorio alberga habilidades modulares listas para producción, diseñadas para operar de manera fluida en diversos agentes y entornos de IA, incluidos **Claude Code**, **Google Antigravity**, **Cursor**, **OpenAI Codex** y **Orca**.

---

## 📦 Catálogo de Habilidades

| Habilidad | Categoría | Descripción | Entornos Compatibles |
| :--- | :--- | :--- | :--- |
| [`android-sanitizer`](./plugins/android-sanitizer/) | Utilidades / Móvil | Triaje autónomo de dispositivos Android, remediación de adware/pop-ups, desinstalación de bloatware de fabricantes (Xiaomi, Samsung, Motorola, Transsion) y configuración automática de bloqueo de publicidad vía DNS Privado. | Claude Code, Antigravity, Cursor, Codex, Orca |

---

## 🚀 Instalación y Uso

### 1. En Claude Code (vía Marketplace)
Registra este repositorio como marketplace en Claude Code:
```bash
/plugin marketplace add diogofrj/fulltech-platform-skills
```
Instala la habilidad deseada:
```bash
/plugin install android-sanitizer
```

### 2. En Google Antigravity / Entornos con Agent Skills
Copia o crea un enlace simbólico de la carpeta de la habilidad en el directorio de agentes:
```bash
# Nivel global de usuario (disponible en todos los workspaces)
cp -r plugins/android-sanitizer ~/.agents/skills/
```

### 3. Vía CLI Abierto de Skills (`skills.sh`)
```bash
npx skills add diogofrj/fulltech-platform-skills@android-sanitizer
```

---

## 🛠️ Arquitectura del Repositorio

Este repositorio adopta un **estándar híbrido multi-harness**:

```text
fulltech-platform-skills/
├── .claude-plugin/
│   └── marketplace.json            # Catálogo indexador de Claude Code / Claude Hub
├── plugins/
│   └── android-sanitizer/          # Habilidad de triaje y limpieza Android
│       ├── .claude-plugin/
│       │   └── plugin.json         # Manifiesto de plugin para Claude
│       ├── SKILL.md                # Instrucciones universales para agentes
│       ├── scripts/
│       │   ├── triage.sh           # Utilidad POSIX bash
│       │   └── triage.ps1          # Utilidad Windows PowerShell
│       └── references/
│           └── oem_catalog.json    # Catálogo de motores de anuncios y bloatware por fabricante
├── README.md                       # Documentación en Inglés
├── README.pt-BR.md                 # Documentación en Portugués de Brasil
└── README.es.md                    # Documentación en Español
```

---

## 🤝 Cómo Contribuir

1. Crea un nuevo directorio para la habilidad dentro de `plugins/<nombre-de-la-habilidad>`.
2. Sigue el formato estándar `SKILL.md` (frontmatter YAML con nombre y descripción + instrucciones estructuradas).
3. Incluye scripts auxiliares en `scripts/` (compatibles tanto con POSIX `sh` como con PowerShell, según corresponda).
4. Registra el nuevo plugin en el archivo `.claude-plugin/marketplace.json`.

---

© Fulltech Engineering. Todos los derechos reservados.

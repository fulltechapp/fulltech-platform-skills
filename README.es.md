# Fulltech Platform Skills

<p align="center">
  <strong>🌐 Documentación Multi-Idioma</strong><br>
  <a href="README.md"><b>English</b></a> •
  <a href="README.pt-BR.md"><b>Português (Brasil)</b></a> •
  <a href="README.es.md"><b>Español</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Arquitectura-Multi--Harness-blue?style=for-the-badge&logo=anthropic" alt="Multi-Harness" />
  <img src="https://img.shields.io/badge/Claude%20Code-Compatible-8A2BE2?style=for-the-badge" alt="Claude Code" />
  <img src="https://img.shields.io/badge/Google%20Antigravity-Compatible-4285F4?style=for-the-badge&logo=google" alt="Google Antigravity" />
  <img src="https://img.shields.io/badge/skills.sh-Ecosistema-green?style=for-the-badge" alt="Skills.sh" />
  <img src="https://img.shields.io/badge/Licencia-MIT-lightgrey?style=for-the-badge" alt="Licencia" />
</p>

---

> **Marketplace empresarial de Agent Skills, Ingeniería DevOps y Análisis Forense de Dispositivos para Fulltech.**

Este repositorio alberga habilidades modulares listas para producción, diseñadas para operar de manera fluida en diversos agentes y entornos de IA: **Claude Code**, **Google Antigravity**, **Cursor**, **OpenAI Codex** y **Orca**.

---

## 🌟 Habilidad Destacada: `android-sanitizer`

> *"¿Por qué el teléfono de tu abuela con el 100% de batería parecía completamente muerto hasta que se conectaba al USB?"*

La mayoría de los desinstaladores de bloatware para Android son listas estáticas de paquetes. **`android-sanitizer`** es un **agente forense de triaje autónomo** que se conecta mediante ADB, audita informes de colapso del sistema (*tombstones*) en tiempo real, diagnostica bloqueos de controladores a nivel de hardware y rehabilita dispositivos.

### 🔬 Caso de Estudio Real: El "Sleep of Death" (SOD) Causado por Adware

Durante las pruebas en un dispositivo con procesador Snapdragon 660 (Redmi Note 7), el teléfono experimentó el clásico **Sueño de la Muerte (Sleep of Death)**:
- La batería estaba al **100% (4,39 V)**, pero el botón de encendido no podía encender la pantalla de ninguna manera.
- Conectar el cable USB generaba una interrupción física de 5V en el chip PMIC que forzaba el encendido de la pantalla.

`android-sanitizer` consultó el historial de fallos del sistema (`dumpsys dropbox`) e identificó al culpable con precisión quirúrgica:

```text
Timestamp: 2026-09-06 21:38:38-0300
Process: >>> /system/vendor/bin/mm-pp-dpps <<<
Signal: 6 (SIGABRT)
Abort message: 'Attempted to retrieve value from failed HIDL call: Status(EX_TRANSACTION_FAILED): DEAD_OBJECT'
```

**La Secuencia Forense:**
1. Entre las `21:03` y las `21:35`, se produjo una instalación en cascada de juegos gratuitos con anuncios de video invasivos.
2. A las `21:38`, cuando la pantalla se apagó, los buffers de video acelerados por hardware (`SurfaceView`) colisionaron con el Carrusel de Fondos de Pantalla de Xiaomi (`fashiongallery`) intentando proyectar anuncios en la pantalla de bloqueo.
3. El servicio de post-procesamiento de pantalla de Qualcomm (`mm-pp-dpps`) entró en *deadlock* y colapsó con `DEAD_OBJECT`.
4. **Remediación:** La eliminación de los generadores de anuncios de pantalla de bloqueo y de la cadena de juegos resolvió el SOD de forma definitiva, liberando **~300 MB de RAM** y constatando una **retención de salud de batería del 98% (3.923 mAh / 4.000 mAh)**.

---

## 📊 Comparativa: Debloaters Estáticos vs. `android-sanitizer`

| Capacidad | Debloaters Tradicionales (UAD, Canta) | `android-sanitizer` (Agent Skill) |
| :--- | :---: | :---: |
| **Triaje Conversacional** | ❌ No | ✅ **Agente de IA Autónomo** |
| **Diagnóstico de Sleep-of-Death (SOD)** | ❌ No | ✅ **Audita tombstones y `mm-pp-dpps`** |
| **Detección de Cascada ("Punto Azul")** | ❌ No | ✅ **Agrupa cadenas de anuncios por fecha/hora** |
| **Cuestionario Interactivo con el Usuario** | ❌ No | ✅ **Decisiones guiadas mediante `ask_question`** |
| **Cuidado para Adultos Mayores (Protege Juegos/Bancos)**| ❌ Riesgo de rotura | ✅ **Preserva juegos, neutraliza anuncios** |
| **Análisis de Desgaste y Salud de Batería** | ❌ No | ✅ **Capacidad real (mAh) vs. Diseño** |
| **Automatización de Sinkhole vía DNS Privado** | ❌ Manual | ✅ **Lanzador de Intent automático en pantalla** |
| **Arquitectura Multi-Harness** | ❌ Solo GUI aislada | ✅ **Claude Code, Antigravity, Codex, Cursor** |

---

## 📦 Catálogo de Habilidades

| Habilidad | Categoría | Descripción | Entornos Compatibles |
| :--- | :--- | :--- | :--- |
| [`android-sanitizer`](./plugins/android-sanitizer/) | Informática Forense Móvil / Optimización | Triaje autónomo de dispositivos Android, remediación de adware, diagnóstico de SOD, eliminación de bloatware de fabricantes (Xiaomi, Samsung, Motorola, Transsion) y sinkhole de anuncios vía DNS Privado. | Claude Code, Antigravity, Cursor, Codex, Orca |

---

## 🚀 Instalación y Uso

### 1. En Claude Code (vía Marketplace)
Registra este repositorio como marketplace en Claude Code:
```bash
/plugin marketplace add fulltechapp/fulltech-platform-skills
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
npx skills add fulltechapp/fulltech-platform-skills@android-sanitizer
```

---

## 🛠️ Arquitectura del Repositorio

Este repositorio adopta un **estándar híbrido multi-harness**:

```text
fulltech-platform-skills/
├── .claude-plugin/
│   └── marketplace.json            # Catálogo indexador de Claude Code / Claude Hub
├── plugins/
│   └── android-sanitizer/          # Habilidad de triaje forense y limpieza Android
│       ├── .claude-plugin/
│       │   └── plugin.json         # Manifiesto de plugin para Claude
│       ├── SKILL.md                # Instrucciones universales para agentes
│       ├── scripts/
│       │   ├── triage.sh           # Utilidad POSIX bash (--health, --sod, --watch)
│       │   └── triage.ps1          # Utilidad Windows PowerShell (-HealthCheck, -AuditSOD)
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

# Sanitizador y Diagnóstico de Rendimiento para iOS (iPhone / iPad)

<p align="center">
  <strong>🌐 Documentación Multilingüe</strong><br>
  <a href="README.md"><b>English</b></a> •
  <a href="README.pt-BR.md"><b>Português (Brasil)</b></a> •
  <a href="README.es.md"><b>Español</b></a>
</p>

Una skill autónoma para agentes de IA para diagnosticar, sanitizar y optimizar dispositivos Apple iOS (iPhone, iPad) conectados mediante cable USB o Wi-Fi Lockdown sin Jailbreak.

---

## 🎯 Aspectos Destacados

- **Diagnóstico de Batería BMS y Ciclos Reales:** Lee ciclos reales de carga, capacidad de fábrica y capacidad medida en mAh directo del microcontrolador de la batería vía IORegistry (`AppleSmartIOBattery`).
- **Detección de Estrangulamiento de CPU (Throttling):** Identifica cuando iOS reduce dinámicamente la velocidad del procesador por desgaste de la batería (>1000 ciclos o <80% de salud).
- **Auditoría de Pánico de Kernel (`Panic Full`) y Memoria:** Revisa el directorio `/Panics` e informes `JetsamEvent` para validar la integridad de la placa madre y la memoria RAM.
- **Inventario y Purga de Aplicaciones:** Detecta y desinstala aplicaciones residuales de migración (ej. `CopyMyData`) y trampas de suscripción.
- **Auditoría de Perfiles Maliciosos:** Inspecciona y elimina perfiles MDM no autorizados y certificados sospechosos.
- **Bloqueador Nativo de Anuncios (.mobileconfig):** Configura DNS cifrado (DoH) nativo para bloquear anuncios en juegos y Safari sin apps VPN.

---

## 📂 Estructura

- [`SKILL.md`](./SKILL.md) — Instrucciones principales y flujo de triaje en 5 pasos para agentes.
- [`scripts/triage.ps1`](./scripts/triage.ps1) — Script de ejecución y diagnóstico en PowerShell.
- [`scripts/triage_helper.py`](./scripts/triage_helper.py) — Motor asíncrono en Python con `pymobiledevice3` v11+.
- [`scripts/serve_profile.py`](./scripts/serve_profile.py) — Servidor HTTP local para instalación en Safari.
- [`profiles/adguard_dns.mobileconfig`](./profiles/adguard_dns.mobileconfig) — Perfil de configuración de DNS cifrado.
- [`references/ios_bundle_catalog.json`](./references/ios_bundle_catalog.json) — Catálogo de apps y redes publicitarias abusivas.

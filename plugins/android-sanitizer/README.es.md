# Android Sanitizer & Limpieza de Adware

<p align="center">
  <strong>🌐 Documentación Multi-Idioma</strong><br>
  <a href="README.md"><b>English</b></a> •
  <a href="README.pt-BR.md"><b>Português (Brasil)</b></a> •
  <a href="README.es.md"><b>Español</b></a>
</p>

Una habilidad inteligente y multi-harness para diagnosticar, desinfectar y proteger dispositivos Android conectados mediante ADB.

---

## 🎯 Puntos Clave

- **Modo Cuidado para Adultos Mayores y Usuarios Casuales:** Preserva juegos casuales (Candy Crush, Mahjong, Solitario), aplicaciones bancarias, médicas y personales intactas mientras silencia los anuncios a través de un sinkhole de DNS Privado.
- **Detección Forense de Ventanas:** Identifica al instante qué aplicación está mostrando anuncios en pantalla en tiempo real mediante `dumpsys window`.
- **Auditoría de Superposición y Accesibilidad:** Localiza aplicaciones que abusan de `SYSTEM_ALERT_WINDOW` y servicios de accesibilidad.
- **Eliminación de Adware Nativo de Fabricantes:** Catálogo optimizado para Xiaomi (HyperOS/MIUI), Samsung (One UI), Motorola y Transsion.
- **Sinkhole mediante DNS Privado:** Facilita la configuración de AdGuard DNS (`dns.adguard-dns.com`) para bloquear anuncios de video y rastreadores en todas las apps y navegadores.

---

## 📂 Archivos de la Habilidad

- [`SKILL.md`](./SKILL.md) — Instrucciones principales y flujo de trabajo para agentes de IA.
- [`scripts/triage.sh`](./scripts/triage.sh) — Script utilitario en Bash (Linux/WSL/macOS).
- [`scripts/triage.ps1`](./scripts/triage.ps1) — Script utilitario en PowerShell (Windows).
- [`references/oem_catalog.json`](./references/oem_catalog.json) — Base de datos de motores publicitarios y bloatware por fabricante.

# Higienizador Linux (Linux + WSL)

<p align="center">
  <strong>🌐 Documentación Multilingüe</strong><br>
  <a href="README.md"><b>English</b></a> •
  <a href="README.pt-BR.md"><b>Português (Brasil)</b></a> •
  <a href="README.es.md"><b>Español</b></a>
</p>

Una habilidad para agentes de IA que realiza triaje de solo lectura y limpieza con dry-run primero en sistemas Ubuntu/Debian, incluidas distros que corren en WSL.

---

## 🎯 Destacados

- **Detección automática del entorno:** bare metal, VM, contenedor, WSL1 y WSL2; las comprobaciones se adaptan a cada uno.
- **Recuperación de espacio:** caché de apt, journal de systemd, revisiones antiguas de snaps; Docker y `~/.cache` se reportan, nunca se borran.
- **Desactivación de telemetría:** apport, whoopsie, popularity-contest, ubuntu-report, motd-news (desactivados, no purgados, para no eliminar metapaquetes).
- **Compatible con WSL:** lee `wsl.conf`, detecta contaminación del PATH de Windows y se niega a editar un `/etc/hosts` generado automáticamente.
- **Seguro por defecto:** la remediación es dry-run salvo que se pase `--apply` con sudo.

---

## 📂 Estructura

- [`SKILL.md`](./SKILL.md) — Instrucciones y flujo para agentes.
- [`scripts/triage.sh`](./scripts/triage.sh) — Triaje de solo lectura, genera `linux_triage.json`.
- [`scripts/remediate.sh`](./scripts/remediate.sh) — Remediación (dry-run por defecto).
- [`scripts/generate_report.py`](./scripts/generate_report.py) — Informe HTML (design system fulltech.app).

> El lado Windows de WSL (compactación de `ext4.vhdx`, `.wslconfig`) está en [`windows-sanitizer`](../windows-sanitizer/) (`-CompactWslDisks`).

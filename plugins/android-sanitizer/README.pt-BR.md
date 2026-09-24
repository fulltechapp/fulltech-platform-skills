# Android Sanitizer & Limpeza de Adwares

<p align="center">
  <strong>🌐 Documentação Multi-Idioma</strong><br>
  <a href="README.md"><b>English</b></a> •
  <a href="README.pt-BR.md"><b>Português (Brasil)</b></a> •
  <a href="README.es.md"><b>Español</b></a>
</p>

Uma skill inteligente e multi-harness para diagnosticar, higienizar e proteger celulares Android conectados via ADB.

---

## 🎯 Destaques

- **Modo Cuidado com Idosos e Usuários Casuais:** Mantém joguinhos casuais (Candy Crush, Mahjong, Paciência), bancos, saúde e redes sociais intactos enquanto silencia as propagandas por meio de sinkhole de DNS Privado.
- **Detecção Forense de Janelas:** Identifica no flagra qual aplicativo está projetando anúncios na tela em tempo real via `dumpsys window`.
- **Auditoria de Sobreposição e Acessibilidade:** Localiza apps que abusam de `SYSTEM_ALERT_WINDOW` e serviços de acessibilidade.
- **Remoção de Adwares Nativos de Fabricantes:** Catálogo curado para Xiaomi (HyperOS/MIUI), Samsung (One UI), Motorola e Transsion.
- **Sinkhole via DNS Privado:** Facilita a configuração do AdGuard DNS (`dns.adguard-dns.com`) para barrar anúncios em vídeo e rastreadores em todos os apps e navegadores.

---

## 📂 Arquivos da Skill

- [`SKILL.md`](./SKILL.md) — Instruções principais e fluxo de raciocínio para agentes de IA.
- [`scripts/triage.sh`](./scripts/triage.sh) — Script utilitário em Bash (Linux/WSL/macOS).
- [`scripts/triage.ps1`](./scripts/triage.ps1) — Script utilitário em PowerShell (Windows).
- [`references/oem_catalog.json`](./references/oem_catalog.json) — Catálogo de pacotes de adwares e bloatwares por fabricante.

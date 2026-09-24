# Higienizador Linux (Linux + WSL)

<p align="center">
  <strong>🌐 Documentação Multilíngue</strong><br>
  <a href="README.md"><b>English</b></a> •
  <a href="README.pt-BR.md"><b>Português (Brasil)</b></a> •
  <a href="README.es.md"><b>Español</b></a>
</p>

Uma skill para agentes de IA que faz triagem somente leitura e limpeza com dry-run primeiro em sistemas Ubuntu/Debian, incluindo distros rodando no WSL.

---

## 🎯 Destaques

- **Detecção automática de ambiente:** bare metal, VM, container, WSL1 e WSL2; as checagens se adaptam a cada um.
- **Recuperação de espaço:** cache do apt, journal do systemd, revisões antigas de snaps; Docker e `~/.cache` são reportados, nunca apagados.
- **Desativação de telemetria:** apport, whoopsie, popularity-contest, ubuntu-report, motd-news (desativados, não removidos, para não derrubar metapacotes).
- **Ciente do WSL:** lê `wsl.conf`, aponta poluição do PATH do Windows e se recusa a editar um `/etc/hosts` gerado automaticamente.
- **Seguro por padrão:** a remediação é dry-run a menos que `--apply` seja passado com sudo.

---

## 📂 Estrutura

- [`SKILL.md`](./SKILL.md) — Instruções e fluxo para agentes.
- [`scripts/triage.sh`](./scripts/triage.sh) — Triagem somente leitura, gera `linux_triage.json`.
- [`scripts/remediate.sh`](./scripts/remediate.sh) — Remediação (dry-run por padrão).
- [`scripts/generate_report.py`](./scripts/generate_report.py) — Relatório HTML (design system fulltech.app).

> O lado Windows do WSL (compactação do `ext4.vhdx`, `.wslconfig`) fica no [`windows-sanitizer`](../windows-sanitizer/) (`-CompactWslDisks`).

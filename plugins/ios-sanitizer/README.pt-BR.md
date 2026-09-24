# Higienizador e Diagnóstico de Performance para iOS (iPhone / iPad)

<p align="center">
  <strong>🌐 Documentação Multilíngue</strong><br>
  <a href="README.md"><b>English</b></a> •
  <a href="README.pt-BR.md"><b>Português (Brasil)</b></a> •
  <a href="README.es.md"><b>Español</b></a>
</p>

Uma skill autônoma para agentes de IA para diagnosticar, higienizar e otimizar dispositivos Apple iOS (iPhone, iPad) conectados via cabo USB ou Wi-Fi Lockdown sem necessidade de Jailbreak.

---

## 🎯 Destaques

- **Raio-X de Bateria e Ciclos Reais (BMS):** Lê contagem exata de ciclos, capacidade nominal medida em mAh, capacidade de fábrica e temperatura diretamente do chip de gerenciamento da bateria via IORegistry (`AppleSmartIOBattery`).
- **Diagnóstico de Throttling da CPU (Gerenciamento de Desempenho):** Detecta quando o iOS reduz a velocidade do chip Apple A-Series devido ao desgaste físico da bateria (>1000 ciclos ou <80% de saúde).
- **Auditoria de Pânico de Hardware (`Panic Full`) e Memória:** Inspeciona o diretório `/Panics` e relatórios `JetsamEvent` para atestar a integridade física da placa-mãe e estouramento de RAM.
- **Inventário de Apps e Purga de Resíduos:** Identifica e desinstala apps residuais de migração (como `CopyMyData`) e assinaturas predatórias.
- **Auditoria de Perfis Maliciosos:** Inspeciona e remove perfis de gerenciamento remoto (MDM), proxies e certificados espiões.
- **Bloqueador de Anúncios Nativo (Ad-Sinkhole via .mobileconfig):** Configura DNS criptografado DoH nativo da Apple (AdGuard DNS) para bloquear anúncios em jogos e no Safari com zero consumo de bateria e sem apps de VPN.

---

## 📂 Estrutura

- [`SKILL.md`](./SKILL.md) — Instruções completas e fluxo de triagem em 5 etapas para agentes de IA.
- [`scripts/triage.ps1`](./scripts/triage.ps1) — Script de execução e diagnóstico autônomo em PowerShell.
- [`scripts/triage_helper.py`](./scripts/triage_helper.py) — Motor assíncrono em Python utilizando `pymobiledevice3` v11+.
- [`scripts/serve_profile.py`](./scripts/serve_profile.py) — Servidor HTTP local para instalação do perfil em 1 clique via Safari.
- [`profiles/adguard_dns.mobileconfig`](./profiles/adguard_dns.mobileconfig) — Payload do perfil de DNS criptografado da Apple.
- [`references/ios_bundle_catalog.json`](./references/ios_bundle_catalog.json) — Catálogo de apps e redes de anúncios abusivas.

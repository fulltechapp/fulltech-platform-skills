# Fulltech Platform Skills - Guidelines & Context

## Project Architecture
This repository contains multi-harness agent skills and plugins for device forensics, optimization, and adware remediation across Android and iOS.

- `plugins/android-sanitizer`: ADB-based forensics, Sleep-of-Death (`mm-pp-dpps`) diagnosis, OEM catalog, and Private DNS sinkhole.
- `plugins/linux-sanitizer`: Bash triage/remediation for Ubuntu/Debian with automatic WSL mode (`wsl.conf`, Windows PATH, generated hosts). Host-side WSL (vhdx compaction, `.wslconfig`) lives in `windows-sanitizer`.
- `plugins/ios-sanitizer`: Apple Lockdown protocol (`pymobiledevice3` v11+ async), BMS raw battery register extraction (cycles, capacity, temperature), Apple CPU Dynamic Throttling detection, `/Panics` inspection, residual app purge, and native Apple `.mobileconfig` DNS sinkhole.
- `generate_report.py`: Standalone HTML artifact generator using the official **fulltech.app Design System** (Geist/JetBrains Mono, `#090A0F` background, `#11131A` cards, `#10B981` emerald, `#38BDF8` cyan). Focused on human-readable consultative verdicts.

## Connected Systems
- **FTM MCP Server:** `https://ftm.fulltech.app/mcp`
- **Supported Harnesses:** Claude Code, Google Antigravity, Cursor, OpenAI Codex, Orca.

<!-- guardiao-baseline:start -->
## Baseline de conformidade do Guardião Fulltech

A baseline canônica fica em `~/projetos/00-Guidelines/baseline/CATALOGO.md` (versão fixada em `baseline/VERSION`); procedimentos em `baseline/ADOTAR.md` e `baseline/VERIFICACAO.md`. Não replique nem edite a baseline dentro deste projeto.

- Gatilho manual: quando o usuário disser **“sincronizar aderência com o Guardião”** (ou **“atualizar conformidade do Guardião”**), carregue a skill global `guardian-sync`, faça o de-para completo dos controles da versão fixada contra este projeto e atualize o painel central. Execute o mesmo fluxo ao fechar uma etapa de integração/publicação/operação e quando uma mudança afetar controles, evidências, arquitetura, dados, identidade, exposição, dependências ou fornecedores.
- Leia o catálogo e os critérios de aceite; examine o estado real do projeto e evidências. Para cada controle, registre ID, aplicabilidade, estado, justificativa, dono e evidência. Distinga documentado, implementado, testado e implantado. Não marque `verified` apenas porque existe um documento; use `unknown` quando a evidência ou a revisão for insuficiente. Exclusões e exceções exigem justificativa e responsável conforme o catálogo.
- Mantenha `docs/compliance/guardiao-baseline.md` como de-para legível deste projeto: versão da baseline, revisão avaliada, data, revisor e tabela dos controles com status, justificativa e caminhos de evidência. Atualize-o sem substituir ou duplicar documentação de domínio existente.
- Atualize `~/projetos/00-Guidelines/monitor/assessments/<nome-exato-da-pasta-do-projeto>.json`, que alimenta a aderência exibida no portal. Preserve este formato: `baseline_version`, `project_revision` (SHA completo de `git rev-parse HEAD`), `assessed_at` (ISO 8601 UTC) e `controls` com um registro por ID contendo `id`, `applicability` (`applicable`, `not_applicable` ou `unknown`), `status` (`verified`, `missing`, `planned`, `implemented`, `exception` ou `unknown`), `reason`, `owner` e `evidence` (lista). Cada evidência verificada deve ter `path`, `revision` igual ao SHA avaliado, `verified_at`, `expires_at`, `outcome: "passed"` e `reviewer`; o arquivo precisa existir no commit avaliado e satisfazer o procedimento do controle. Registre explicitamente o que não foi avaliado; não infira conformidade.
- Depois execute `python3 ~/projetos/00-Guidelines/monitor/guardian.py build` para atualizar `~/projetos/00-Guidelines/index.html` e `monitor/output/index.html`. Confira o projeto no portal e relate aderência, cobertura, itens verificados e pendências com seus links. Como o registro exige a revisão atual, mudanças no HEAD podem tornar a avaliação anterior desconhecida até nova sincronização.
- Se a avaliação revelar controles aplicáveis `missing`, `planned` ou `implemented`, ou achados tecnológicos confirmados, solicite uma segunda opinião automaticamente antes de concluir: `python3 ~/projetos/00-Guidelines/monitor/guardian.py consult --project <nome-exato-da-pasta> --model codex-astra`. Essa consulta envia somente IDs/descrições dos controles pendentes e metadados/resumos/fontes dos achados confirmados; nunca envie conteúdo de arquivos ou segredos. Use `--model claude-fable` quando o usuário escolher Claude (Fable com fallback Opus), ou `--model codex-sol` quando escolher GPT-6.1-Sol e a autenticação atual aceitar o modelo. Se a consulta falhar, mantenha erro e pendências explícitos. Parecer é consultivo, nunca evidência nem autorização. Controles apenas desconhecidos não disparam consulta. Ao concluir, execute `python3 ~/projetos/00-Guidelines/monitor/guardian.py build` novamente para incorporar o resultado no portal.
<!-- guardiao-baseline:end -->

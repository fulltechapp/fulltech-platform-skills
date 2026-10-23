# Spec: ft-progresso

Mod do Claude Code que mostra, acima do prompt e no painel `/progresso`, o andamento dos planos de
um repo, lendo os quatro formatos de board em uso na Fulltech. Derivado do mod `progresso` do JP Labs
(MIT, commit `5f37a15` de `thejplabs-ai/jp-labs-skills`), com a paleta do Design System Fulltech.

## Problema

Os repos da Fulltech guardam estado de trabalho em quatro lugares diferentes: Backlog.md (padrão
atual), tickets do BMad (`_bmad-output/**/tickets.toml`), `.devtool/` (Kanban Markdown, legado) e
`progresso.md` (formato do JP Labs). Saber "o que falta e qual é o próximo" exige abrir cada um.

## Fontes e ordem de verdade

| Fonte | Detecção | Lote (barra) | Item | Escrita pelo agente |
|---|---|---|---|---|
| Backlog.md | `backlog/config.yml` | milestone (wave) | task em `backlog/tasks` e `backlog/completed` | só CLI `backlog` |
| BMad | `_bmad/method/scripts/tickets.py` | epic da iniciativa ativa | ticket (`tickets.py status`) | `tickets.py mark` |
| .devtool | `.devtool/features/` | `epic` do frontmatter | card | `.devtool/card.sh` se existir; migrar ao trabalhar |
| progresso.md | raiz, `plans/*/`, `.aios/plans/sprints/*/` | `##` | `- [ ]` | edição direta |

Mapa de estado (comum): feito, andando, esperando (com `quem`), falta. `dropped`/arquivado fica de
fora da conta.

- Backlog.md: `Done` feito; `In Progress`/`In Review` andando; status com `block`/`wait`/`esper`
  esperando (quem = assignee); resto falta. `backlog/completed` conta como feito.
- BMad: `done` feito; `review`/`in-progress` andando; `status=blocked` ou `blocked_at` esperando
  (quem = `blocked_reason`); `planned`/`backlog` falta; `dropped` fora.
- .devtool: `done` feito; `doing`/`review` andando; `blocked` esperando (quem = label `quem:`); resto falta.

## Regras do mod

- Leitura só do disco do projeto e de um processo opcional: `python3 tickets.py status` (BMad) e
  `gh pr list` (progresso.md com `pr:N`). Sem rede própria, sem escrita em disco.
- Regra no prompt só para as fontes presentes, dizendo como atualizar cada uma (CLI, nunca editar
  `backlog/*.md` na mão).
- A skill `ft-progresso` não cria `progresso.md` em repo que já tem Backlog.md ou BMad.

## Waves

- W1 (sequencial): parsers puros das quatro fontes com teste; mod com faixa, painel e regra;
  skill; README de instalação; marketplace. DoD: `claude plugin validate` e `claude plugin test`
  verdes, `tsc` limpo, smoke manual num repo com Backlog.md.

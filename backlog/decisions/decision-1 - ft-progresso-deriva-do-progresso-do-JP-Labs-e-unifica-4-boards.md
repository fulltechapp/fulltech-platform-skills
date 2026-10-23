---
id: decision-1
title: ft-progresso deriva do progresso do JP Labs e unifica 4 boards
date: '2026-10-23 02:36'
status: accepted
---
## Context

Repos da Fulltech têm estado de trabalho em Backlog.md, tickets BMad, `.devtool/` e `progresso.md`. O mod `progresso` do JP Labs (MIT, `5f37a15`) foi auditado em 2026-10-22: só lê `progresso.md` e roda `gh pr list`; sem rede nem escrita. Instalado puro, a skill dele cria `progresso.md` em todo plano e duplica o Backlog.md.

## Decision

Criar o plugin `ft-progresso` neste marketplace, derivado do `progresso` (créditos e licença MIT mantidos), lendo as quatro fontes com um mapa de estado único (docs/ft-progresso/spec.md) e a paleta do DS Fulltech. A regra no prompt e a skill mandam atualizar cada fonte pela ferramenta dela (CLI `backlog`, `tickets.py mark`, `card.sh`) e nunca criam `progresso.md` em repo com Backlog.md ou BMad.

## Consequences

- Uma faixa só por repo, independente do board.
- Dependência leve de `python3` (BMad) e `gh` (PRs), ambas opcionais: sem elas a fonte some, o resto segue.
- Mudança de formato do Backlog.md ou do `tickets.py` quebra só o parser daquela fonte; testes por fonte pegam isso.


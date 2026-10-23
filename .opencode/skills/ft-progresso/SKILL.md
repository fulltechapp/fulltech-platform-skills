---
name: ft-progresso
description: "Mantém verdadeiro o board do projeto: Backlog.md, tickets BMad, .devtool ou progresso.md. Use ao montar um plano com mais de uma etapa, quando o usuário pedir pra acompanhar o progresso, ou quando o estado de um item do plano mudar."
license: MIT
compatibility: opencode
metadata:
  source: plugins/ft-progresso/skills/ft-progresso/SKILL.md
---

# ft-progresso

O plugin `ft-progresso` do Claude Code lê o board do projeto e mostra quanto do plano foi feito e
qual é o próximo item. No OpenCode só esta skill está disponível: a faixa e o painel `/progresso`
não existem. Aqui ela serve para escolher o board certo e mantê-lo verdadeiro.

## Qual board usar

Na ordem, o primeiro que o projeto tiver:

1. **Backlog.md** (`backlog/config.yml`): wave = milestone, card = task. Tudo pela CLI `backlog`,
   nunca editando os `.md` de `backlog/` à mão (o corpo de decisão é a única exceção).
2. **BMad** (`_bmad/`): tickets da iniciativa ativa em `_bmad-output/**/tickets.toml`; status por
   `python3 _bmad/method/scripts/tickets.py mark <ref> <status>`.
3. **.devtool** (legado): mova cards com `.devtool/card.sh <id> <status>` se existir. Ao trabalhar
   no repo, proponha migrar os cards para o Backlog.md.
4. **progresso.md**: só em projeto sem nenhum dos anteriores. Nunca crie `progresso.md` ao lado de
   Backlog.md ou BMad: seria uma segunda fonte de verdade.

Projeto novo sem board: o padrão Fulltech é Backlog.md
(`backlog init <nome> --defaults --integration-mode cli --agent-instructions none`).

## Marcar o estado

| Estado | Backlog.md | BMad | .devtool | progresso.md |
|---|---|---|---|---|
| começou | `backlog task edit <id> -s "In Progress"` | `mark <ref> in-progress` | `card.sh <id> doing` | `[~]` |
| em revisão | `-s "In Review"` (se a config tiver) | `mark <ref> in-review` | `card.sh <id> review` | `[~]` |
| esperando alguém | status de bloqueio da config, com `-a <quem>` | `mark <ref> blocked --blocked "<motivo>"` | `card.sh <id> blocked` + label `quem:<x>` | `[!] ...  quem: <x>` |
| terminou | `-s Done` + `--check-ac <n>` | `mark <ref> done` | `card.sh <id> done` | `[x]` + evidência |

## Regras

- **Mude o estado no mesmo passo em que ele muda**, nunca em lote no fim da sessão.
- **Só marque feito com prova desta sessão** (teste rodado, PR mergeado, arquivo entregue) e deixe
  a evidência: nota final da task no Backlog.md, `pr:N`/hash/data no `progresso.md`.
- Item novo entra no lote (milestone, epic, `##`) certo, não no fim.
- Item que caiu de escopo sai (arquivar no Backlog.md, `dropped` no BMad) e você avisa o usuário no
  mesmo passo; parado como pendente, a barra conta como falta pra sempre.

## Formato do progresso.md

```markdown
# Progresso: <título do plano>

## L0 <primeira fase>
- [x] Plano escrito e aprovado
- [~] <entrega em andamento>
- [!] <coisa que depende de alguém>  quem: você
- [ ] <próxima entrega>  pr:12
```

Fica na raiz (um plano) ou em `plans/<nome-do-plano>/progresso.md` (vários). `##` é um lote, na
ordem de execução; a primeira palavra (mais o número, se houver) vira o rótulo usado pelo plugin do
Claude Code.

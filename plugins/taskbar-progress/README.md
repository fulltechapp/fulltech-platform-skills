# taskbar-progress

Mod do Claude Code que mostra, acima do prompt, quanto do plano do repo já foi feito e qual é o
próximo item, e abre um painel com tudo em `/progresso`. Lê os quatro boards em uso na Fulltech:

| Board | Onde ele procura | Lote (barra) | Item |
|---|---|---|---|
| **Backlog.md** | `backlog/config.yml`, `backlog/tasks`, `backlog/completed`, `backlog/milestones` | milestone (wave) | task |
| **BMad** | `_bmad/method/scripts/tickets.py status` (iniciativa ativa) | epic | ticket |
| **.devtool** (legado) | `.devtool/features` e `features/done` | `epic` | card |
| **superpowers** | `docs/superpowers/plans/*.md` (um plano = um card) | `### Task N` | passo `- [ ]` (o 1º aberto de task começado conta como andando) |
| **EGM** (Elephant Goldfish Model) | `consolidated_review_report.md` e `goldfish_review_report.md`, na raiz ou em `docs/designs/` | prioridade 🔴 Blocker / 🟡 Major / 🟢 Nit | achado (`Status: resolved` no topo, `[x]` ou ✅ fecham). Melhor esforço |
| **progresso.md** | raiz, `plans/<plano>/`, `.aios/plans/sprints/<plano>/` | `##` | `- [ ]` |

- **Faixa acima do prompt:** uma linha por plano vivo (até 3), com a barra do lote em curso, o
  total e o próximo item. O plano com item em andamento vem primeiro, marcado com `▸`.
- **Painel `/progresso`:** um cartão por plano com o anel de %, a origem (`[backlog]`, `[bmad]`,
  `[devtool]`, `[md]`), a barra de cada lote e os itens dos lotes abertos.
- **Barra de tarefas / aba do terminal:** o % geral dos planos vivos aparece na barra de tarefas ou na
  aba (OSC 9;4: Windows Terminal, Ghostty, iTerm2, ConEmu), em âmbar quando algo espera você; some
  quando não há plano vivo ou a sessão termina. Desligue em `/config` (`taskbar`). Dentro do tmux a
  sequência não passa.
- **Esperando você** em âmbar: item bloqueado com você no `quem:` / assignee.
- **Confere com o GitHub:** item de `progresso.md` com `pr:N` é conferido pelo `gh`.
- **Regra no prompt:** só para os boards que o repo tem, dizendo como atualizar cada um (CLI
  `backlog`, `tickets.py mark`, `card.sh`). Nunca cria `progresso.md` em repo com Backlog.md ou BMad.
- Paleta do Design System Fulltech (`#090A0F`, `#11131A`, emerald `#10B981`, cyan `#38BDF8`).

Estados no mapa comum: feito, andando (`In Progress`/`In Review`, `review`/`in-progress`,
`doing`/`review`, `[~]`), esperando (status de bloqueio, `blocked`, `[!]`) e falta.

## Instalar

Precisa do Claude Code 2.1.287 ou mais novo (`claude --version`).

Dentro do Claude Code, uma linha (adiciona o marketplace se faltar; responda `y`):

```
/plugin install taskbar-progress --marketplace fulltechapp/fulltech-platform-skills
```

Ou em dois passos, se o marketplace já estiver adicionado:

```
/plugin marketplace add fulltechapp/fulltech-platform-skills
/plugin install taskbar-progress@fulltech-platform-skills
```

Escolha o escopo quando ele perguntar:

- **user**: vale para todo repo. Seguro com o fluxo Fulltech, porque a skill escolhe o board que o
  repo já tem e não cria `progresso.md` ao lado de Backlog.md/BMad.
- **project**: só no repo atual.

Fora do Claude Code (terminal):

```
claude plugin marketplace add fulltechapp/fulltech-platform-skills
claude plugin install taskbar-progress@fulltech-platform-skills
```

Depois de instalar, rode `/reload-plugins` (ou abra uma sessão nova). Verificar: num repo com
Backlog.md a faixa aparece acima do prompt e `/progresso` abre o painel.

Atualizar: `/plugin marketplace update fulltech-platform-skills`. Remover: `/plugin uninstall taskbar-progress`.

**Teu nome no `quem:`** (opcional): por padrão `você`, `eu` e `me` contam como esperando você.
Para o assignee do Backlog.md (ex.: `@diogo`) contar também, ponha `diogo` em `/config`, na linha
do `taskbar-progress`.

## O que ele acessa

Mod roda com o teu acesso. Este aqui:

- **lê** só os arquivos dos quatro boards listados acima, na raiz do projeto;
- **roda** dois comandos, ambos de leitura e opcionais: `python3 _bmad/method/scripts/tickets.py status`
  (só em repo com `_bmad/`, no máximo a cada 30 s) e `gh pr list` (só se algum `progresso.md` tiver
  `pr:N`, a cada 5 min). Sem `python3` ou sem `gh`, aquela fonte para e o resto segue;
- **escreve no contexto do Claude** a regra de manter os boards verdadeiros, só nos repos que têm board;
- **escreve** uma única sequência de controle (OSC 9;4, o % da barra de tarefas) em `/dev/tty` via
  `sh -c printf`, só quando o % muda e se a opção `taskbar` estiver ligada (padrão); falha em silêncio
  sem tty;
- **não** acessa a internet, **não** escreve em disco e **não** guarda nada fora da sessão.

## Desenvolvimento

```
claude plugin validate plugins/taskbar-progress
claude plugin test plugins/taskbar-progress
```

Parsers puros em `hooks/parse.ts` (progresso.md, placar, faixa) e `hooks/fontes.ts` (Backlog.md,
BMad, .devtool), cada um com teste. Spec em `docs/taskbar-progress/spec.md`.

## Créditos e licença

Derivado do mod [`progresso`](https://github.com/thejplabs-ai/jp-labs-skills/tree/main/progresso)
do JP Labs (MIT, commit `5f37a15`). MIT, ver `LICENSE`.

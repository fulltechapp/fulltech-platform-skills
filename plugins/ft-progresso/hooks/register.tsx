// register.tsx — o mod `ft-progresso`: faixa acima do prompt com uma linha por plano vivo, painel
// /progresso com um cartão por plano (DS Fulltech: anel de %, barras no degradê emerald -> cyan, o
// feixe atravessando a barra ao abrir e ao fechar item), conferência de PR pelo gh e a regra de manter
// cada board verdadeiro no prompt (só para os boards que o projeto tem). Derivado do `progresso` do
// JP Labs (MIT); as fontes Backlog.md, BMad e .devtool estão em fontes.ts.

import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Origem, Sprint } from '../types'
import { parseBacklog, parseBmad, parseDevtool, type Arquivo } from './fontes'
import { barra, estadoReal, linhasDaFaixa, parseProgresso, placar, quemVoce } from './parse'
import { ANEL, anelCells, barraCells } from './raster'

const PANE = 'progresso'
const sprints = atom({ plugin: 'ft-progresso', key: 'sprints' } as const, [])
const prs = atom({ plugin: 'ft-progresso', key: 'prs' } as const, {})

const RELER_MS = 10_000
const GH_MS = 5 * 60_000
const BMAD_MS = 30_000
const TICKETS = '_bmad/method/scripts/tickets.py'
const BARRA = 26 // colunas da barra de lote no painel
const QUADRO_MS = 33
const FEIXE_QUADROS = 36 // ~1,2s

// onde o mod procura: `progresso.md` na raiz, ou um por plano numa destas pastas
const PASTAS = ['plans', '.aios/plans/sprints']

// a regra de cada board, só dos que o projeto tem; cada um é atualizado pela ferramenta dele
const REGRAS: Record<Origem, (voce: string) => string> = {
  backlog: () => 'Backlog.md (`backlog/`): mude o status só pela CLI (`backlog task edit <id> -s "In Progress"` ao começar, `-s Done` ao terminar, `--check-ac <n>` por critério cumprido), nunca editando os `.md` de `backlog/` à mão.',
  bmad: () => `Tickets BMad da iniciativa ativa: status por \`python3 ${TICKETS} mark <ref> <in-progress|in-review|done>\` (travado: \`--blocked "<motivo>"\`).`,
  devtool: () => 'Board legado `.devtool/`: mova o card com `.devtool/card.sh <id> <status>` se existir; ao trabalhar neste repo, proponha migrar os cards para o Backlog.md.',
  progresso: (voce) => `\`progresso.md\` (raiz, \`plans/<plano>/\`): começou -> \`[~]\`; esperando alguém -> \`[!]\` com \`quem: <${voce} | pessoa | data>\` no fim; terminou -> \`[x]\` com a evidência na linha (\`pr:N\`, hash, data).`,
}
const regra = (origens: ReadonlySet<Origem>, voce: string): string => [
  'O usuário acompanha os planos deste projeto numa faixa acima do prompt e no /progresso. Mantenha cada board verdadeiro no mesmo passo em que o estado muda:',
  ...(['backlog', 'bmad', 'devtool', 'progresso'] as const).filter((o) => origens.has(o)).map((o) => `- ${REGRAS[o](voce)}`),
  'Só marque feito com teste ou prova desta sessão. Item novo entra no lote certo. Não crie `progresso.md` em projeto que já tem Backlog.md ou BMad.',
].join('\n')

// DS Fulltech: emerald é o acento, cyan o andamento, âmbar só em ação
const C = {
  fundo: '#090A0F', card: '#11131A', borda: '#1E2230', bordaForte: '#2D3348', ink: '#F8FAFC', body: '#CBD5E1', muted: '#94A3B8',
  apagado: '#475569', acento: '#10B981', claro: '#38BDF8', ambar: '#F59E0B', erro: '#F43F5E', trilho: '#1E2230',
}
const SELO: Record<Origem, string> = { progresso: 'md', backlog: 'backlog', bmad: 'bmad', devtool: 'devtool' }
const ICONE: Record<string, string> = { feito: '✓', andando: '◐', esperando: '⏳', falta: '○', diverge: '✗' }

// estado do módulo: recomeça a cada carga, o que importa fica em $.state
let raiz = ''
let voce = quemVoce()
let repoOk = true
let bmadOk = true
let bmadEm = -Infinity
let bmadUltimo: Sprint | null = null
// arquivo -> texto já lido, pela mtime da listagem: o Backlog.md de um repo grande não é relido inteiro a cada 10s
const cache = new Map<string, { mtimeMs: number; texto: string }>()
let feitosAntes: Record<string, number> = {}
let animando: { cancel: () => void } | null = null

const chaveBarra = (pasta: string, lote: number) => `barra:${pasta}:${lote}`
const chaveAnel = (pasta: string) => `anel:${pasta}`

/** O feixe atravessa a barra do lote em curso de cada sprint em `alvo`, e o anel enche até o %. */
function feixeNoPainel($: EngineInterface, alvo: readonly Sprint[], mapa: Readonly<Record<string, string>>, encherAnel: boolean): void {
  animando?.cancel()
  const passos = alvo.map((s) => {
    const p = placar(s, mapa, voce)
    const li = p.lotes.findIndex((l) => l.feitos < l.total)
    const lote = li >= 0 ? p.lotes[li] : p.lotes[p.lotes.length - 1]
    const pct = p.total === 0 ? 0 : (p.feitos / p.total) * 100
    return { s, li: li >= 0 ? li : p.lotes.length - 1, lote, pct }
  })
  let q = 0
  const timer = $.clock.every(QUADRO_MS, () => {
    q++
    const t = Math.min(1, q / FEIXE_QUADROS)
    for (const x of passos) {
      if (x.lote) {
        const cheio = x.lote.total === 0 ? 0 : Math.round((x.lote.feitos / x.lote.total) * BARRA)
        const brilho = t >= 1 || cheio === 0 ? null : Math.floor(t * (cheio + 2)) - 1
        void $.ui.blit({ requestId: PANE, key: chaveBarra(x.s.pasta, x.li), columns: BARRA, rows: 1, cells: barraCells(x.lote.feitos, x.lote.total, BARRA, brilho) })
      }
      if (encherAnel) {
        const e = 1 - Math.pow(1 - t, 3) // ease-out
        void $.ui.blit({ requestId: PANE, key: chaveAnel(x.s.pasta), columns: ANEL.colunas, rows: ANEL.linhas, cells: anelCells(x.pct * e) })
      }
    }
    if (t >= 1) { timer.cancel(); if (animando === timer) animando = null }
  })
  animando = timer
}

/** Os `.md` de uma pasta, relendo só o que mudou desde a última listagem. */
async function mds($: EngineInterface, dir: string): Promise<Arquivo[]> {
  const ents = (await $.fs.list(dir).catch(() => [])).filter((e) => e.kind === 'file' && e.name.endsWith('.md'))
  const out: Arquivo[] = []
  for (const e of ents) {
    const arq = `${dir}/${e.name}`
    let c = cache.get(arq)
    if (c === undefined || c.mtimeMs !== e.mtimeMs) {
      c = { mtimeMs: e.mtimeMs, texto: await $.fs.read(arq).catch(() => '') }
      cache.set(arq, c)
    }
    out.push({ nome: e.name, texto: c.texto, mtimeMs: e.mtimeMs })
  }
  return out
}

const existe = async ($: EngineInterface, p: string): Promise<boolean> => (await $.fs.stat(p).catch(() => undefined)) !== undefined

/** Backlog.md: `backlog/config.yml` marca o board; tasks + completed, agrupadas por milestone. */
async function lerBacklog($: EngineInterface): Promise<Sprint | null> {
  const base = `${raiz}/backlog`
  const config = await $.fs.read(`${base}/config.yml`).catch(() => undefined)
  if (config === undefined) return null
  const s = parseBacklog(config, await mds($, `${base}/milestones`), await mds($, `${base}/tasks`), await mds($, `${base}/completed`))
  return s.lotes.length > 0 ? s : null
}

/** BMad: a iniciativa ativa pelo próprio `tickets.py status`, no máximo a cada BMAD_MS. */
async function lerBmad($: EngineInterface): Promise<Sprint | null> {
  if (!bmadOk || !(await existe($, `${raiz}/${TICKETS}`))) return null
  const agora = await $.clock.now()
  if (agora - bmadEm < BMAD_MS) return bmadUltimo
  bmadEm = agora
  const r = await $.process.run(['python3', TICKETS, 'status'], { cwd: raiz, timeoutMs: 15_000 }).catch(() => undefined)
  if (r === undefined) return bmadUltimo
  if (r.exitCode !== 0) {
    bmadOk = false // sem python3, sem iniciativa ativa ou árvore malformada: para nesta carga
    return (bmadUltimo = null)
  }
  const s = parseBmad(r.stdout, agora)
  return (bmadUltimo = s && s.lotes.length > 0 ? s : null)
}

/** .devtool: cards abertos e os de `done/`. */
async function lerDevtool($: EngineInterface): Promise<Sprint | null> {
  const base = `${raiz}/.devtool/features`
  const cards = [...(await mds($, base)), ...(await mds($, `${base}/done`))]
  return cards.length > 0 ? parseDevtool(cards) : null
}

async function reler($: EngineInterface): Promise<void> {
  if (raiz === '') return
  const achados = [{ nome: raiz.split(/[\\/]/).filter(Boolean).pop() ?? 'projeto', arq: `${raiz}/progresso.md` }]
  for (const pasta of PASTAS) {
    const base = `${raiz}/${pasta}`
    const dentro = (await $.fs.list(base).catch(() => [])).filter((p) => p.kind === 'dir')
    for (const p of dentro) achados.push({ nome: p.name, arq: `${base}/${p.name}/progresso.md` })
  }
  const lidos: Sprint[] = []
  for (const { nome, arq } of achados) {
    const st = await $.fs.stat(arq).catch(() => undefined)
    if (st === undefined) continue
    const texto = await $.fs.read(arq).catch(() => '')
    lidos.push(parseProgresso(nome, texto, st.mtimeMs))
  }
  for (const s of [await lerBacklog($), await lerBmad($), await lerDevtool($)]) if (s !== null) lidos.push(s)
  await update($, sprints, () => lidos)
  // item que fechou desde a última leitura: o feixe passa na barra daquele sprint
  const mapa = await read($, prs)
  const agora: Record<string, number> = {}
  const subiram: Sprint[] = []
  for (const s of lidos) {
    agora[s.pasta] = placar(s, mapa, voce).feitos
    const antes = feitosAntes[s.pasta]
    if (antes !== undefined && (agora[s.pasta] ?? 0) > antes) subiram.push(s)
  }
  feitosAntes = agora
  if (subiram.length > 0) feixeNoPainel($, subiram, mapa, false)
}

async function conferePRs($: EngineInterface): Promise<void> {
  if (raiz === '' || !repoOk) return
  const lista = await read($, sprints)
  if (!lista.some((s) => s.lotes.some((l) => l.itens.some((i) => i.pr !== null)))) return
  const r = await $.process
    .run(['gh', 'pr', 'list', '--state', 'all', '--limit', '300', '--json', 'number,state'], { cwd: raiz })
    .catch(() => undefined)
  if (r === undefined) return
  if (r.exitCode !== 0) {
    repoOk = false // sem gh ou repo sem GitHub: para de tentar nesta carga
    return
  }
  try {
    const arr = JSON.parse(r.stdout) as Array<{ number: number; state: string }>
    const mapa: Record<string, string> = {}
    for (const x of arr) mapa[String(x.number)] = x.state
    await update($, prs, () => mapa)
  } catch {
    // saída que não é JSON: fica a última leitura
  }
}

export const register: Register = (on, options) => {
  const nome = typeof options.nome === 'string' ? options.nome.trim() : ''
  voce = quemVoce(nome)
  const quem = nome || 'você'

  on('session.start', async ($, e, next) => {
    // nome tomado (outra skill ou plugin): fica sem o comando, mas a faixa e a regra seguem
    await $.command.register({ name: 'progresso', description: 'Abre o painel com o que foi feito e o que falta de cada plano' }).catch(() => undefined)
    raiz = await $.session.root()
    await reler($)
    await conferePRs($)
    $.clock.every(RELER_MS, () => { void reler($) })
    $.clock.every(GH_MS, () => { void conferePRs($) })
    return next(e)
  })

  on('command.run', { command: 'progresso' }, async $ => {
    await reler($)
    await conferePRs($)
    const lista = await read($, sprints)
    if (lista.length === 0) return { text: 'Nenhum plano neste projeto (Backlog.md, BMad, .devtool ou progresso.md). Peça pro Claude montar o plano e a faixa aparece.' }
    await $.ui.open({ id: PANE, title: 'Progresso' })
    const mapa = await read($, prs)
    // o painel monta no próximo quadro: o feixe começa logo depois
    $.clock.after(120, () => feixeNoPainel($, lista.filter((s) => !placar(s, mapa, voce).completo), mapa, true))
    return { text: 'Painel de progresso aberto.' }
  })

  on('prompt.compose', async ($, e, next) => {
    const r = await next(e)
    const origens = new Set((await read($, sprints)).map((s) => s.origem))
    if (origens.size === 0) return r
    return { sections: [...r.sections, { id: 'ft-progresso:regra', text: regra(origens, quem), scope: 'session' }] }
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey) return next(e)
    const { linhas, resto } = linhasDaFaixa(await read($, sprints), await read($, prs), voce)
    if (linhas.length === 0) return next(e)
    const { Box, Text } = $.ui.resolve(e)
    const largura = Math.max(...linhas.map((l) => l.nome.length))
    return (
      <Box flexDirection="column">
        {linhas.map((l, i) => {
          const b = l.lote ? barra(l.lote.feitos, l.lote.total, 10) : barra(l.feitos, l.total, 10)
          return (
            <Text key={l.nome} wrap="truncate-end">
              <Text color={C.acento}>{l.ativo ? '▸ ' : '  '}</Text>
              <Text color={l.ativo ? C.ink : C.body} weight={l.ativo ? 'bold' : 'regular'}>{l.nome.padEnd(largura)}</Text>
              {'  '}
              {l.lote ? <Text color={C.muted}>{l.lote.nome} </Text> : null}
              <Text color={C.acento}>{b.cheio}</Text>
              <Text color={C.trilho}>{b.vazio}</Text>
              <Text color={C.muted}> {l.lote ? `${l.lote.feitos}/${l.lote.total}` : ''} · {l.feitos}/{l.total}</Text>
              {l.esperandoVoce > 0 ? <Text color={C.ambar} weight="bold">  ⏳ {l.esperandoVoce} esperando você</Text> : null}
              {l.esperandoOutro ? <Text color={C.muted}>  ⏳ {l.esperandoOutro.n} {l.esperandoOutro.quem}</Text> : null}
              {l.diverge > 0 ? <Text color={C.erro}>  ✗ {l.diverge} diverge</Text> : null}
              {l.proximo ? <Text color={C.body}>  › {l.proximo}</Text> : null}
              {i === linhas.length - 1 && resto > 0 ? <Text color={C.muted}>  +{resto}</Text> : null}
            </Text>
          )
        })}
      </Box>
    )
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const el = $.ui.resolve(e)
    const { Box, Text } = el
    const Raster = 'Raster' in el ? el.Raster : null // só o terminal tem; nos outros, o painel fica sem anel e barra
    const mapa = await read($, prs)
    const lista = [...(await read($, sprints))].sort((a, b) => {
      const pa = placar(a, mapa, voce), pb = placar(b, mapa, voce)
      return Number(pa.completo) - Number(pb.completo) || Number(pb.ativo) - Number(pa.ativo) || b.mtimeMs - a.mtimeMs
    })
    if (lista.length === 0) {
      return (
        <Box backgroundColor={C.fundo} paddingX={1}>
          <Text color={C.muted}>Nenhum plano neste projeto.</Text>
        </Box>
      )
    }
    return (
      <Box flexDirection="column" backgroundColor={C.fundo} paddingX={1} paddingY={1}>
        {lista.map((s) => {
          const p = placar(s, mapa, voce)
          const pct = p.total === 0 ? 0 : (p.feitos / p.total) * 100
          const emCurso = p.lotes.find((l) => l.feitos < l.total)
          const outros = Object.entries(p.esperandoOutros).sort((a, b) => b[1] - a[1])
          return (
            <Box key={s.pasta} flexDirection="column" backgroundColor={C.card} borderStyle="round" borderColor={p.ativo ? C.acento : C.borda} paddingX={2} paddingY={1} marginBottom={1}>
              <Box flexDirection="row">
                {Raster ? <Raster key={chaveAnel(s.pasta)} columns={ANEL.colunas} rows={ANEL.linhas} cells={anelCells(pct)} /> : null}
                <Box flexDirection="column" paddingLeft={2} justifyContent="center">
                  <Text wrap="truncate-end">
                    <Text color={C.ink} weight="bold">{s.titulo}</Text>
                    <Text color={C.muted}>  [{SELO[s.origem]}]</Text>
                  </Text>
                  <Text color={C.body}>
                    {p.feitos} de {p.total}{p.completo ? '  ·  completo' : emCurso ? `  ·  ${emCurso.nome} em curso` : ''}
                  </Text>
                  {p.esperandoVoce > 0 ? <Text color={C.ambar} weight="bold">⏳ {p.esperandoVoce} esperando você</Text> : null}
                  {outros.length > 0 ? <Text color={C.muted} wrap="truncate-end">⏳ {outros.map(([q, n]) => `${n} ${q}`).join(' · ')}</Text> : null}
                  {p.diverge > 0 ? <Text color={C.erro}>✗ {p.diverge} diverge do GitHub</Text> : null}
                </Box>
              </Box>
              {p.completo ? null : s.lotes.map((l, li) => {
                const pl = p.lotes[li]
                const feitos = pl?.feitos ?? 0, total = pl?.total ?? 0
                const fechado = total > 0 && feitos === total
                return (
                  <Box key={`${s.pasta}/${l.nome}`} flexDirection="column" marginTop={1}>
                    <Box flexDirection="row">
                      <Text color={fechado ? C.muted : C.ink} weight="bold">{l.nome.padEnd(28).slice(0, 28)} </Text>
                      {Raster ? <Raster key={chaveBarra(s.pasta, li)} columns={BARRA} rows={1} cells={barraCells(feitos, total, BARRA)} /> : null}
                      <Text color={C.muted}>  {feitos}/{total}</Text>
                    </Box>
                    {fechado ? null : l.itens.map((it, i) => {
                      const est = estadoReal(it, mapa)
                      const st = it.pr === null ? undefined : mapa[String(it.pr)]
                      const daVoce = est === 'esperando' && it.quem !== null && voce.test(it.quem)
                      const corIcone = est === 'feito' ? C.acento : est === 'andando' ? C.claro : est === 'diverge' ? C.erro : est === 'esperando' ? (daVoce ? C.ambar : C.body) : C.apagado
                      const corTexto = est === 'feito' ? C.muted : est === 'diverge' ? C.erro : est === 'andando' ? C.ink : C.body
                      return (
                        <Text key={`${s.pasta}/${l.nome}/${i}`} wrap="truncate-end">
                          <Text color={corIcone}>  {ICONE[est]}  </Text>
                          <Text color={corTexto} weight={est === 'andando' ? 'bold' : 'regular'}>{it.texto}</Text>
                          {it.pr !== null ? <Text color={st === 'MERGED' ? C.acento : C.muted}>  #{it.pr}</Text> : null}
                          {it.quem !== null && est !== 'feito' ? <Text color={daVoce ? C.ambar : C.muted}>  {it.quem}</Text> : null}
                        </Text>
                      )
                    })}
                  </Box>
                )
              })}
            </Box>
          )
        })}
      </Box>
    )
  })
}

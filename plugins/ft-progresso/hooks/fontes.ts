// fontes.ts — Backlog.md, tickets do BMad e o board .devtool virando Sprint, no mesmo mapa de estado
// do progresso.md (docs/ft-progresso/spec.md). Puro: sem $.

import type { Estado, Item, Lote, Sprint } from '../types'

type Valor = string | string[] | null

/** Frontmatter YAML raso: `chave: valor`, listas `[a, b]` ou em bloco `- a`. O resto é ignorado. */
export function frontmatter(texto: string): Record<string, Valor> {
  const fm: Record<string, Valor> = {}
  const linhas = texto.split(/\r?\n/)
  if (linhas[0]?.trim() !== '---') return fm
  let lista: string | null = null
  for (const linha of linhas.slice(1)) {
    if (linha.trim() === '---') break
    const item = /^\s+-\s+(.*)$/.exec(linha)
    if (item && lista !== null) {
      ;(fm[lista] as string[]).push(semAspas(item[1] ?? ''))
      continue
    }
    const kv = /^([A-Za-z_][\w-]*):\s*(.*)$/.exec(linha)
    if (!kv) continue
    const chave = kv[1] ?? '', v = (kv[2] ?? '').trim()
    lista = null
    if (v === '') { fm[chave] = []; lista = chave }
    else if (v.startsWith('[')) fm[chave] = v.slice(1, v.lastIndexOf(']')).split(',').map(semAspas).filter((x) => x !== '')
    else fm[chave] = v === 'null' || v === '~' ? null : semAspas(v)
  }
  return fm
}

const semAspas = (s: string): string => s.trim().replace(/^(['"])(.*)\1$/, '$2')
const texto = (v: Valor | undefined): string => (typeof v === 'string' ? v : '')
const lista = (v: Valor | undefined): string[] => (Array.isArray(v) ? v : typeof v === 'string' && v !== '' ? [v] : [])

/** Agrupa itens em lotes na ordem em que cada lote aparece primeiro. */
function agrupa(pares: ReadonlyArray<{ lote: string; item: Item }>): Lote[] {
  const lotes = new Map<string, Item[]>()
  for (const { lote, item } of pares) {
    const l = lotes.get(lote) ?? []
    l.push(item)
    lotes.set(lote, l)
  }
  return [...lotes].map(([nome, itens]) => ({ nome, itens }))
}

const item = (t: string, estado: Estado, quem: string | null): Item => ({ texto: t, estado, pr: null, quem })

// ── Backlog.md ──────────────────────────────────────────────────────────────────────────────────

export type Arquivo = { nome: string; texto: string; mtimeMs: number }

const ESPERA = /block|wait|esper|aguard|bloq/i

/** O status do Backlog.md no mapa comum: o último da config é feito, o primeiro é falta. */
export function estadoBacklog(status: string, statuses: readonly string[]): Estado {
  const s = status.toLowerCase()
  const ultimo = (statuses[statuses.length - 1] ?? 'Done').toLowerCase()
  const primeiro = (statuses[0] ?? 'To Do').toLowerCase()
  if (s === ultimo || s === 'done') return 'feito'
  if (s === primeiro || s === '') return 'falta'
  if (ESPERA.test(s)) return 'esperando'
  return 'andando'
}

/**
 * Um Sprint por repo: lote = milestone (na ordem m-0, m-1...), item = task. `completed` conta como
 * feito; task sem milestone cai em "Sem wave", no fim.
 */
export function parseBacklog(config: string, milestones: readonly Arquivo[], tasks: readonly Arquivo[], completas: readonly Arquivo[]): Sprint {
  const cfg = frontmatter(`---\n${config}\n---`)
  const statuses = lista(cfg.statuses)
  const nomes = new Map<string, string>()
  const ordem = new Map<string, number>()
  for (const m of milestones) {
    const fm = frontmatter(m.texto)
    const id = texto(fm.id)
    if (id === '') continue
    nomes.set(id.toLowerCase(), texto(fm.title) || id)
    ordem.set(id.toLowerCase(), Number(/(\d+)$/.exec(id)?.[1] ?? 1e9))
  }
  const pares: Array<{ lote: string; item: Item; n: number; ord: number }> = []
  let mtimeMs = 0
  for (const [arqs, completa] of [[tasks, false], [completas, true]] as const) {
    for (const a of arqs) {
      const fm = frontmatter(a.texto)
      if (texto(fm.id) === '') continue
      mtimeMs = Math.max(mtimeMs, a.mtimeMs)
      const ms = texto(fm.milestone)
      const chave = ms.toLowerCase()
      const estado = completa ? 'feito' : estadoBacklog(texto(fm.status), statuses)
      const quem = lista(fm.assignee).map((x) => x.replace(/^@/, '')).join(', ') || null
      pares.push({
        lote: ms === '' ? 'Sem wave' : nomes.get(chave) ?? ms,
        item: item(`${texto(fm.id)} ${texto(fm.title)}`.trim(), estado, estado === 'esperando' ? quem : null),
        n: ms === '' ? 2e9 : ordem.get(chave) ?? 1e9,
        ord: Number(texto(fm.ordinal) || /(\d+)/.exec(texto(fm.id))?.[1] || 0),
      })
    }
  }
  pares.sort((a, b) => a.n - b.n || a.ord - b.ord)
  return { origem: 'backlog', pasta: 'backlog', titulo: texto(cfg.project_name) || 'Backlog', lotes: agrupa(pares), mtimeMs }
}

// ── BMad ────────────────────────────────────────────────────────────────────────────────────────

type Ticket = { epic?: string; title?: string; ref?: string; status?: string; state?: string; blocked_at?: string; blocked_reason?: string }

/** A saída de `tickets.py status` (iniciativa ativa): lote = epic, item = ticket, em ordem de build. */
export function parseBmad(json: string, mtimeMs: number): Sprint | null {
  let r: { folder?: string; tickets?: Ticket[] }
  try { r = JSON.parse(json) as typeof r } catch { return null }
  if (!Array.isArray(r.tickets)) return null
  const pares: Array<{ lote: string; item: Item }> = []
  for (const t of r.tickets) {
    if (t.state === 'dropped' || t.status === 'dropped') continue
    const bloqueado = t.status === 'blocked' || (t.blocked_at ?? '') !== ''
    const estado: Estado = t.state === 'done' ? 'feito'
      : bloqueado ? 'esperando'
      : t.state === 'review' || t.state === 'in-progress' ? 'andando'
      : 'falta'
    const epic = (t.epic ?? '').replace(/^epic-/, '') || 'Tickets'
    pares.push({ lote: epic, item: item(`${t.ref ?? ''} ${t.title ?? ''}`.trim(), estado, bloqueado ? t.blocked_reason || 'bloqueado' : null) })
  }
  const pasta = `bmad:${(r.folder ?? 'iniciativa').replace(/^initiative-/, '')}`
  return { origem: 'bmad', pasta, titulo: r.folder ?? 'BMad', lotes: agrupa(pares), mtimeMs }
}

// ── .devtool (Kanban Markdown, legado) ──────────────────────────────────────────────────────────

/** O status do card no mapa comum: colunas backlog/todo/doing/review/done (+ blocked). */
export function estadoDevtool(status: string): Estado {
  const s = status.toLowerCase()
  if (s === 'done') return 'feito'
  if (s === 'blocked' || ESPERA.test(s)) return 'esperando'
  if (s === 'doing' || s === 'review' || s === 'in-progress') return 'andando'
  return 'falta'
}

/** Cards de `.devtool/features` e `features/done`: lote = `epic`, item = card, na ordem do `order`. */
export function parseDevtool(cards: readonly Arquivo[]): Sprint {
  let mtimeMs = 0
  const pares = cards.map((c) => {
    mtimeMs = Math.max(mtimeMs, c.mtimeMs)
    const fm = frontmatter(c.texto)
    const id = texto(fm.id) || c.nome.replace(/\.md$/, '')
    const h1 = /^#\s+(.+)$/m.exec(c.texto)?.[1]?.trim() ?? id
    const titulo = h1.replace(new RegExp(`^${id.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\s*[—–:-]\\s*`, 'i'), '')
    const estado = estadoDevtool(texto(fm.status))
    const quem = lista(fm.labels).find((l) => l.startsWith('quem:'))?.slice(5) || texto(fm.assignee) || null
    return { lote: texto(fm.epic) || 'Cards', item: item(`${id} ${titulo}`, estado, estado === 'esperando' ? quem : null), ord: texto(fm.order) || id }
  })
  pares.sort((a, b) => a.ord.localeCompare(b.ord))
  return { origem: 'devtool', pasta: '.devtool', titulo: '.devtool (legado)', lotes: agrupa(pares), mtimeMs }
}

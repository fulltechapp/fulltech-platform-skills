import type { Register } from 'claude-code'

const fmt = (ms: number) => {
  const s = Math.round(ms / 1000)
  return s < 60 ? `${s}s` : `${Math.floor(s / 60)}m${String(s % 60).padStart(2, '0')}s`
}
const clip = (t: string, n: number) => {
  const one = t.replace(/\s+/g, ' ').trim()
  return one.length > n ? one.slice(0, n - 1) + '…' : one
}

const agents = new Map<string, string>() // agentId -> descrição do subagente
const busy = new Map<string, string>() // loop -> o que faz agora ('' = sessão principal)

function show($: { ui: { status: (t: string | undefined) => void } }) {
  if (busy.size === 0) return $.ui.status(undefined)
  const parts: string[] = []
  for (const [k, v] of busy) parts.push(k === '' ? v : `🤖 ${clip(agents.get(k) ?? 'subagente', 18)}: ${v}`)
  $.ui.status('⚙ ' + parts.join(' │ '))
}

export const register: Register = on => {
  const prompts = new Map<string, string>() // turnId -> o que foi pedido

  const target = (e: Record<string, unknown>) => {
    const v = e.command ?? e.file_path ?? e.pattern ?? e.description ?? e.url ?? e.query ?? e.prompt
    return typeof v === 'string' ? clip(v, 40) : ''
  }

  on('tool.call', async ($, e, next) => {
    const k = (e as { agentId?: string }).agentId ?? ''
    busy.set(k, `${e.tool} ${target(e as unknown as Record<string, unknown>)}`.trim())
    show($)
    return next(e)
  }).catch(($, e, next) => next(e))

  on('agent.spawn', async ($, e, next) => {
    const r = await next(e)
    if (r.agentId) agents.set(r.agentId, e.description || e.subagentType)
    return r
  }).catch(($, e, next) => next(e))

  on('turn.start', async ($, e, next) => {
    if (e.agentId === undefined && e.text) prompts.set(e.turnId, e.text)
    return next(e)
  })

  on('turn.complete', async ($, e, next) => {
    const r = await next(e)
    busy.delete(e.agentId ?? '')
    if (e.agentId === undefined) busy.clear()
    show($)
    const isAgent = e.agentId !== undefined
    const what = isAgent
      ? agents.get(e.agentId!) ?? 'subagente'
      : clip(prompts.get(e.turnId) ?? '', 50)
    prompts.delete(e.turnId)

    const bad = e.reason === 'error' || e.reason === 'refusal'
    const asset = bad ? 'sounds/error.wav' : isAgent ? 'sounds/agent.wav' : 'sounds/done.wav'
    if (!e.isAborted) $.audio.play({ asset }).catch(() => {})

    const u = e.usage as { input_tokens?: number; output_tokens?: number } | undefined
    const tok = u ? ` · ${((u.input_tokens ?? 0) + (u.output_tokens ?? 0)).toLocaleString('pt-BR')} tokens` : ''
    const label = e.isAborted ? 'interrompido' : bad ? 'falhou' : 'concluído'
    $.ui.toast(`${isAgent ? '🤖 ' : '✅ '}${label}: ${what} (${fmt(e.durationMs)}${tok})`)
    return r
  })
}

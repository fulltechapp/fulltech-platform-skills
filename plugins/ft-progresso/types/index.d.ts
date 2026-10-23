/** Estado comum das quatro fontes: `[ ]` falta, `[~]` andando, `[!]` esperando, `[x]` feito. */
export type Estado = 'falta' | 'andando' | 'esperando' | 'feito'

/** De onde veio o plano: progresso.md, Backlog.md, tickets do BMad ou o board legado .devtool. */
export type Origem = 'progresso' | 'backlog' | 'bmad' | 'devtool'

export type Item = {
  texto: string
  estado: Estado
  /** `pr:N` no item: conferido no GitHub */
  pr: number | null
  /** de quem o item espera: `quem:` (progresso.md, .devtool), assignee (Backlog.md), blocked_reason (BMad) */
  quem: string | null
}

export type Lote = { nome: string; itens: Item[] }

export type Sprint = {
  origem: Origem
  /** chave única do plano e nome na faixa */
  pasta: string
  titulo: string
  lotes: Lote[]
  mtimeMs: number
}

declare module 'claude-code' {
  interface PluginState {
    'ft-progresso': {
      sprints: Sprint[]
      /** número do PR -> MERGED | OPEN | CLOSED, da última leitura do gh */
      prs: Record<string, string>
    }
  }
}

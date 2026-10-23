import { expect, test } from 'claude-code/testing'

import { estadoBacklog, estadoDevtool, frontmatter, parseBacklog, parseBmad, parseDevtool } from './fontes'
import { placar, rotulo } from './parse'

const arq = (nome: string, texto: string, mtimeMs = 1) => ({ nome, texto, mtimeMs })

test('frontmatter: escalar com e sem aspas, lista inline e em bloco, null', () => {
  const fm = frontmatter('---\nid: "d1"\ntitle: \'a: b\'\nlabels: ["x", "quem:diogo"]\nassignee:\n  - "@ana"\ndueDate: null\n---\n# corpo')
  expect(fm).toEqual({ id: 'd1', title: 'a: b', labels: ['x', 'quem:diogo'], assignee: ['@ana'], dueDate: null })
  expect(frontmatter('sem frontmatter')).toEqual({})
})

test('Backlog.md: status da config no mapa comum', () => {
  const st = ['To Do', 'In Progress', 'In Review', 'Done']
  expect(estadoBacklog('To Do', st)).toBe('falta')
  expect(estadoBacklog('In Progress', st)).toBe('andando')
  expect(estadoBacklog('In Review', st)).toBe('andando')
  expect(estadoBacklog('Blocked', st)).toBe('esperando')
  expect(estadoBacklog('Done', st)).toBe('feito')
  expect(estadoBacklog('Concluído', ['A fazer', 'Concluído'])).toBe('feito')
})

test('Backlog.md: milestone vira lote na ordem, completed conta feito, sem milestone no fim', () => {
  const s = parseBacklog(
    'project_name: "loja"\nstatuses: ["To Do", "In Progress", "Blocked", "Done"]',
    [arq('m-1 - w2.md', '---\nid: m-1\ntitle: "W2 Venda"\n---'), arq('m-0 - w1.md', '---\nid: m-0\ntitle: "W1 Base"\n---')],
    [
      arq('task-3.md', '---\nid: TASK-3\ntitle: checkout\nstatus: To Do\nmilestone: m-1\n---'),
      arq('task-1.md', '---\nid: TASK-1\ntitle: carrinho\nstatus: Blocked\nassignee:\n  - "@diogo"\nmilestone: m-0\n---', 5),
      arq('task-9.md', '---\nid: TASK-9\ntitle: solto\nstatus: In Progress\n---'),
    ],
    [arq('task-2.md', '---\nid: TASK-2\ntitle: produto\nstatus: In Progress\nmilestone: m-0\n---')],
  )
  expect(s.titulo).toBe('loja')
  expect(s.mtimeMs).toBe(5)
  expect(s.lotes.map((l) => l.nome)).toEqual(['W1 Base', 'W2 Venda', 'Sem wave'])
  expect(s.lotes[0]?.itens).toEqual([
    { texto: 'TASK-1 carrinho', estado: 'esperando', pr: null, quem: 'diogo' },
    { texto: 'TASK-2 produto', estado: 'feito', pr: null, quem: null },
  ])
  expect(placar(s, {}).feitos).toBe(1)
  expect(placar(s, {}).proximo?.texto).toBe('TASK-9 solto')
})

test('BMad: epic vira lote, estados do tickets.py, dropped fora, bloqueio com motivo', () => {
  const json = JSON.stringify({
    folder: 'initiative-odin',
    tickets: [
      { epic: 'epic-base', ref: '1.1', title: 'migrações', state: 'done', status: 'done' },
      { epic: 'epic-base', ref: '1.2', title: 'contrato', state: 'review', status: 'built' },
      { epic: 'epic-base', ref: '1.3', title: 'auditoria', state: 'in-progress', status: 'blocked', blocked_reason: 'aguardando Diogo' },
      { epic: 'epic-voz', ref: '2.1', title: 'voz', state: 'planned', status: '' },
      { epic: 'epic-voz', ref: '2.2', title: 'cortado', state: 'dropped', status: 'dropped' },
    ],
  })
  const s = parseBmad(json, 7)
  expect(s?.pasta).toBe('bmad:odin')
  expect(s?.lotes.map((l) => [l.nome, l.itens.map((i) => i.estado)])).toEqual([
    ['base', ['feito', 'andando', 'esperando']],
    ['voz', ['falta']],
  ])
  expect(s?.lotes[0]?.itens[2]?.quem).toBe('aguardando Diogo')
  expect(parseBmad('não é json', 1)).toBe(null)
})

test('.devtool: colunas no mapa comum, título sem o id, quem do label, ordem do order', () => {
  expect(['backlog', 'todo', 'doing', 'review', 'done', 'blocked'].map(estadoDevtool)).toEqual(['falta', 'falta', 'andando', 'andando', 'feito', 'esperando'])
  const s = parseDevtool([
    arq('w2.md', '---\nid: "w2"\nstatus: "todo"\nepic: "waves"\norder: "a02"\n---\n# w2 — Segunda'),
    arq('d1.md', '---\nid: "d1"\nstatus: "blocked"\nepic: "pre"\nlabels: ["quem:diogo"]\norder: "a00"\n---\n# d1 — Domínio'),
    arq('w1.md', '---\nid: "w1"\nstatus: "done"\nepic: "waves"\norder: "a01"\n---\n# w1 — Primeira'),
  ])
  expect(s.lotes.map((l) => l.nome)).toEqual(['pre', 'waves'])
  expect(s.lotes[0]?.itens[0]).toEqual({ texto: 'd1 Domínio', estado: 'esperando', pr: null, quem: 'diogo' })
  expect(s.lotes[1]?.itens.map((i) => i.texto)).toEqual(['w1 Primeira', 'w2 Segunda'])
})

test('rótulo curto do lote', () => {
  expect(['L0 Base', 'Wave VI · CRUD', 'Wave 2a', 'Épico 01a · x', 'Wave EN', 'Histórico (pré)', 'W1 ft-progresso'].map(rotulo))
    .toEqual(['L0', 'Wave VI', 'Wave 2a', 'Épico 01a', 'Wave EN', 'Histórico', 'W1'])
})

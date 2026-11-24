// Draws every <div class="flow" data-flow="key"> on the page with React Flow,
// using the boxes and arrows in flows.json. Needs the import map that build.py
// (and playbook/index.html) put on the page. Each diagram also gets a text
// version, which is all that shows if the libraries can't load.

const FLOWS_URL = new URL('flows.json', import.meta.url)
const STYLE_URL = 'https://cdn.jsdelivr.net/npm/@xyflow/react@13.0.3/dist/style.css'

const CSS = `
.flow { --fn-bg:#ffffff; --fn-ink:#1f2430; --fn-muted:#5d6475; --fn-line:#c3c9d4; --fn-edge:#8a93a3; --fn-canvas:#f7f8fa; --fn-frame:#eef1f6;
  --t-full-bg:#fee4e2; --t-full-line:#d92d20; --t-full-ink:#7a271a;
  --t-std-bg:#d1e9ff; --t-std-line:#2e90fa; --t-std-ink:#194185;
  --t-lite-bg:#d1fadf; --t-lite-line:#039855; --t-lite-ink:#054f31;
  --t-good-bg:#d1fadf; --t-good-line:#039855; --t-good-ink:#054f31;
  --t-orders-bg:#d1e9ff; --t-orders-line:#2e90fa; --t-orders-ink:#194185;
  --t-payments-bg:#fef0c7; --t-payments-line:#dc6803; --t-payments-ink:#93370d;
  --t-warehouse-bg:#ebe9fe; --t-warehouse-line:#7a5af8; --t-warehouse-ink:#3e1c96;
  --t-support-bg:#fce7f6; --t-support-line:#dd2590; --t-support-ink:#851651;
  --t-l10n-bg:#d1fadf; --t-l10n-line:#039855; --t-l10n-ink:#054f31;
  --t-qa-bg:#f2f4f7; --t-qa-line:#667085; --t-qa-ink:#1d2939;
  --t-contract-bg:#ffffff; --t-contract-line:#344054; --t-contract-ink:#1d2939;
  --t-gate-bg:#1d2939; --t-gate-line:#1d2939; --t-gate-ink:#ffffff;
  margin:14px 0; display:flex; flex-direction:column; gap:8px; }
@media (prefers-color-scheme: dark) {
  .flow { --fn-bg:#1c2028; --fn-ink:#e8ebf1; --fn-muted:#a3aab9; --fn-line:#3a4150; --fn-edge:#7d8696; --fn-canvas:#14171d; --fn-frame:#202530;
    --t-full-bg:#55160c; --t-full-line:#f97066; --t-full-ink:#fee4e2;
    --t-std-bg:#102a56; --t-std-line:#53b1fd; --t-std-ink:#d1e9ff;
    --t-lite-bg:#053321; --t-lite-line:#32d583; --t-lite-ink:#d1fadf;
    --t-good-bg:#053321; --t-good-line:#32d583; --t-good-ink:#d1fadf;
    --t-orders-bg:#102a56; --t-orders-line:#53b1fd; --t-orders-ink:#d1e9ff;
    --t-payments-bg:#4e1d09; --t-payments-line:#fdb022; --t-payments-ink:#fef0c7;
    --t-warehouse-bg:#27115f; --t-warehouse-line:#9b8afb; --t-warehouse-ink:#ebe9fe;
    --t-support-bg:#4e0d30; --t-support-line:#f670c7; --t-support-ink:#fce7f6;
    --t-l10n-bg:#053321; --t-l10n-line:#32d583; --t-l10n-ink:#d1fadf;
    --t-qa-bg:#262b35; --t-qa-line:#98a2b3; --t-qa-ink:#e8ebf1;
    --t-contract-bg:#1c2028; --t-contract-line:#98a2b3; --t-contract-ink:#e8ebf1;
    --t-gate-bg:#e8ebf1; --t-gate-line:#e8ebf1; --t-gate-ink:#14171d; }
}
.flow-canvas { border:1px solid var(--fn-line); border-radius:12px; overflow:hidden; background:var(--fn-canvas); }
.flow-canvas .react-flow { --xy-background-color: var(--fn-canvas); }
.flow-cap { font-size:.88rem; color:var(--fn-muted); margin:0; }
.flow-legend { display:flex; flex-wrap:wrap; gap:6px 12px; font-size:.82rem; color:var(--fn-muted); }
.flow-legend span { display:inline-flex; align-items:center; gap:6px; }
.flow-legend i { width:12px; height:12px; border-radius:3px; border:1px solid; }
.flow details { font-size:.88rem; color:var(--fn-muted); }
.flow details summary { cursor:pointer; width:max-content; }
.flow details ul { margin:6px 0 0; padding-left:20px; }
.flow-note { font-size:.88rem; color:var(--fn-muted); margin:0; }
.fn { box-sizing:border-box; padding:9px 12px; border:1.5px solid var(--fn-line); border-radius:8px; background:var(--fn-bg); color:var(--fn-ink);
  font:500 13px/1.35 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; text-align:center;
  display:flex; align-items:center; justify-content:center; box-shadow:0 1px 2px rgba(16,24,40,.06); }
.fn-decision { border-style:dashed; border-width:2px; }
.fn-decision::before { content:"?"; position:absolute; top:-9px; left:-9px; width:18px; height:18px; border-radius:50%;
  background:var(--fn-ink); color:var(--fn-bg); font:700 11px/18px sans-serif; }
.fn-pill { border-radius:999px; }
.fn-circle { border-radius:50%; font-weight:700; }
.fn-result { font-weight:700; }
.fn-frame { background:var(--fn-frame); border:1px dashed var(--fn-line); border-radius:14px; box-shadow:none; align-items:flex-start; justify-content:flex-start;
  color:var(--fn-muted); font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:.05em; padding:10px 14px; }
.fn-contract { border-style:dashed; }
.fn-elabel { position:absolute; pointer-events:none; padding:2px 6px; border-radius:4px; background:var(--fn-canvas);
  color:var(--fn-ink); font:600 12px/1.2 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; white-space:nowrap; }
.fn .react-flow__handle { opacity:0; pointer-events:none; width:6px; height:6px; min-width:0; min-height:0; }
${['full','std','lite','good','orders','payments','warehouse','support','l10n','qa','contract','gate'].map((t) =>
  `.tone-${t} { background:var(--t-${t}-bg); border-color:var(--t-${t}-line); color:var(--t-${t}-ink); }`).join('\n')}
`

function textVersion(flow) {
  const label = (id) => flow.nodes.find((node) => node.id === id).label.replace(/\n/g, ' ')
  const items = flow.edges.map((edge) =>
    `<li>${esc(label(edge.from))} → ${esc(label(edge.to))}${edge.label ? ` <em>(${esc(edge.label)})</em>` : ''}</li>`)
  return `<details><summary>Text version</summary><ul>${items.join('')}</ul></details>`
}

function esc(text) {
  return String(text).replace(/[&<>"]/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch]))
}

// Box sizes from the text, so the layout and the rendered boxes agree.
function sizeOf(node) {
  const lines = node.label.split('\n')
  const longest = Math.max(...lines.map((line) => line.length))
  if (node.kind === 'circle') { const d = Math.max(96, longest * 8 + 30); return { w: d, h: d } }
  const w = Math.min(320, Math.max(node.kind === 'result' ? 110 : 130, longest * 7.1 + 34 + (node.kind === 'decision' ? 10 : 0)))
  return { w, h: Math.max(44, lines.length * 18 + 22) }
}

function layout(flow, dagre) {
  const sizes = Object.fromEntries(flow.nodes.map((node) => [node.id, sizeOf(node)]))
  const pos = {}
  const routes = {}
  if (flow.layout === 'manual') {
    for (const node of flow.nodes) pos[node.id] = { x: node.x, y: node.y }
  } else {
    const g = new dagre.graphlib.Graph()
    g.setGraph({ rankdir: flow.direction, nodesep: 34, ranksep: flow.direction === 'LR' ? 70 : 56, marginx: 10, marginy: 10 })
    g.setDefaultEdgeLabel(() => ({}))
    for (const node of flow.nodes) g.setNode(node.id, { width: sizes[node.id].w, height: sizes[node.id].h })
    for (const edge of flow.edges) {
      g.setEdge(edge.from, edge.to, edge.label ? { label: edge.label, width: edge.label.length * 7 + 12, height: 18 } : {})
    }
    dagre.layout(g)
    for (const node of flow.nodes) {
      const p = g.node(node.id)
      pos[node.id] = { x: p.x - sizes[node.id].w / 2, y: p.y - sizes[node.id].h / 2 }
    }
    flow.edges.forEach((edge, i) => {
      const e = g.edge(edge.from, edge.to)
      routes[i] = { points: e.points, label: edge.label ? { x: e.x, y: e.y } : null }
    })
  }
  return { sizes, pos, routes }
}

// A path through the layout's route points, with rounded corners.
function roundedPath(points, r = 10) {
  let d = `M ${points[0].x} ${points[0].y}`
  for (let i = 1; i < points.length - 1; i++) {
    const [a, b, c] = [points[i - 1], points[i], points[i + 1]]
    const d1 = Math.hypot(b.x - a.x, b.y - a.y), d2 = Math.hypot(c.x - b.x, c.y - b.y)
    const k = Math.min(r, d1 / 2, d2 / 2)
    const p1 = { x: b.x - ((b.x - a.x) / (d1 || 1)) * k, y: b.y - ((b.y - a.y) / (d1 || 1)) * k }
    const p2 = { x: b.x + ((c.x - b.x) / (d2 || 1)) * k, y: b.y + ((c.y - b.y) / (d2 || 1)) * k }
    d += ` L ${p1.x} ${p1.y} Q ${b.x} ${b.y} ${p2.x} ${p2.y}`
  }
  const last = points[points.length - 1]
  return `${d} L ${last.x} ${last.y}`
}

// Connect each arrow on the sides that face each other.
function handlesFor(a, b, sizes, pos) {
  const ax = pos[a].x + sizes[a].w / 2, ay = pos[a].y + sizes[a].h / 2
  const bx = pos[b].x + sizes[b].w / 2, by = pos[b].y + sizes[b].h / 2
  const dx = bx - ax, dy = by - ay
  if (Math.abs(dx) > Math.abs(dy) * 1.2) return dx > 0 ? ['s-right', 't-left'] : ['s-left', 't-right']
  return dy > 0 ? ['s-bottom', 't-top'] : ['s-top', 't-bottom']
}

async function main() {
  const containers = [...document.querySelectorAll('.flow[data-flow]')]
  if (!containers.length) return
  const style = document.createElement('style'); style.textContent = CSS; document.head.append(style)
  const flows = await (await fetch(FLOWS_URL)).json()

  for (const el of containers) {
    const flow = flows[el.dataset.flow]
    if (!flow) { el.innerHTML = `<p class="flow-note">Unknown diagram “${esc(el.dataset.flow)}”.</p>`; continue }
    const legend = flow.legend ? `<div class="flow-legend">${flow.legend.map(([tone, name]) =>
      `<span><i class="tone-${tone}"></i>${esc(name)}</span>`).join('')}</div>` : ''
    el.innerHTML = `<div class="flow-canvas" role="figure" aria-label="${esc(flow.title)}"></div>
      <p class="flow-cap">${esc(flow.title)}</p>${legend}${textVersion(flow)}`
  }

  let lib
  try {
    const link = document.createElement('link'); link.rel = 'stylesheet'; link.href = STYLE_URL; document.head.append(link)
    const [React, { createRoot }, xy, dagreModule] = await Promise.all([
      import('react'), import('react-dom/client'), import('@xyflow/react'), import('@dagrejs/dagre'),
    ])
    lib = { React, createRoot, xy, dagre: dagreModule.default ?? dagreModule }
  } catch (err) {
    console.error(err)
    for (const el of containers) {
      el.querySelector('.flow-canvas')?.replaceWith(Object.assign(document.createElement('p'),
        { className: 'flow-note', textContent: 'The interactive diagram could not load. Open the text version below.' }))
    }
    return
  }

  const { React, createRoot, xy, dagre } = lib
  const h = React.createElement
  const { ReactFlow, Background, Controls, Handle, Position, MarkerType, BaseEdge, EdgeLabelRenderer, getSmoothStepPath } = xy
  const SIDES = [['top', Position.Top], ['bottom', Position.Bottom], ['left', Position.Left], ['right', Position.Right]]

  function Box({ data }) {
    const handles = SIDES.flatMap(([side, position]) => [
      h(Handle, { key: `t-${side}`, id: `t-${side}`, type: 'target', position, isConnectable: false }),
      h(Handle, { key: `s-${side}`, id: `s-${side}`, type: 'source', position, isConnectable: false }),
    ])
    const lines = data.label.split('\n').flatMap((line, i) => (i ? [h('br', { key: `b${i}` }), line] : [line]))
    return h('div', {
      className: `fn fn-${data.kind}${data.tone ? ` tone-${data.tone}` : ''}`,
      style: { width: data.w, height: data.h, position: 'relative' },
    }, ...handles, h('span', null, ...lines))
  }
  function Frame({ data }) {
    return h('div', { className: 'fn fn-frame', style: { width: data.w, height: data.h } }, data.label)
  }
  // Follows the layout's route, which avoids other boxes. Once someone drags
  // one of its boxes, it falls back to a normal step path.
  function Routed(props) {
    const { sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition, data, markerEnd, style, label } = props
    const first = React.useRef({ sourceX, sourceY, targetX, targetY })
    const f = first.current
    const moved = Math.abs(f.sourceX - sourceX) + Math.abs(f.sourceY - sourceY) +
      Math.abs(f.targetX - targetX) + Math.abs(f.targetY - targetY) > 0.5
    let path, lx, ly
    if (!moved && data?.points) {
      path = roundedPath(data.points)
      const mid = data.points[Math.floor(data.points.length / 2)]
      ;({ x: lx, y: ly } = data.label ?? mid)
    } else {
      ;[path, lx, ly] = getSmoothStepPath({ sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition, borderRadius: 10 })
    }
    return h(React.Fragment, null,
      h(BaseEdge, { path, markerEnd, style }),
      label ? h(EdgeLabelRenderer, null, h('div', {
        className: 'fn-elabel nodrag nopan',
        style: { transform: `translate(-50%, -50%) translate(${lx}px, ${ly}px)` },
      }, label)) : null)
  }
  const nodeTypes = { box: Box, frame: Frame }
  const edgeTypes = { routed: Routed }
  const touch = matchMedia('(pointer: coarse)').matches
  const dark = matchMedia('(prefers-color-scheme: dark)')

  for (const el of containers) {
    const flow = flows[el.dataset.flow]
    const canvas = el.querySelector('.flow-canvas')
    if (!flow || !canvas) continue
    const { sizes, pos, routes } = layout(flow, dagre)

    const nodes = [
      ...(flow.frames ?? []).map((frame) => ({
        id: frame.id, type: 'frame', position: { x: frame.x, y: frame.y }, zIndex: -1,
        draggable: false, selectable: false, data: { label: frame.label, w: frame.w, h: frame.h },
      })),
      ...flow.nodes.map((node) => ({
        id: node.id, type: 'box', position: pos[node.id],
        data: { label: node.label, kind: node.kind, tone: node.tone, ...sizes[node.id] },
      })),
    ]
    const edges = flow.edges.map((edge, i) => {
      // flows.json can pin the sides, for arrows that would otherwise cut across a row.
      const [sourceHandle, targetHandle] = edge.handles ?? handlesFor(edge.from, edge.to, sizes, pos)
      return {
        id: `e${i}`, source: edge.from, target: edge.to, sourceHandle, targetHandle, type: 'routed',
        label: edge.label, data: routes[i] ?? null,
        markerEnd: { type: MarkerType.ArrowClosed, color: '#8a93a3', width: 18, height: 18 },
        style: { stroke: 'var(--fn-edge)', strokeWidth: 1.6 },
      }
    })

    // Size the canvas to the drawing's shape.
    const boxes = [...flow.nodes.map((node) => ({ ...pos[node.id], w: sizes[node.id].w, h: sizes[node.id].h })),
      ...(flow.frames ?? []).map((frame) => ({ x: frame.x, y: frame.y, w: frame.w, h: frame.h }))]
    const minX = Math.min(...boxes.map((b) => b.x)), maxX = Math.max(...boxes.map((b) => b.x + b.w))
    const minY = Math.min(...boxes.map((b) => b.y)), maxY = Math.max(...boxes.map((b) => b.y + b.h))
    const width = canvas.clientWidth || 800
    const scale = Math.min(1, (width - 40) / (maxX - minX))
    // Extra height leaves room above the drawing for the zoom buttons.
    canvas.style.height = `${Math.round(Math.min(820, Math.max(220, (maxY - minY) * scale + 120)))}px`

    const root = createRoot(canvas)
    const render = () => root.render(h(ReactFlow, {
      nodes, edges, nodeTypes, edgeTypes,
      colorMode: dark.matches ? 'dark' : 'light',
      fitView: true, fitViewOptions: { padding: 0.1, maxZoom: 1 },
      minZoom: 0.2, maxZoom: 2,
      nodesConnectable: false, elementsSelectable: false, nodesDraggable: true,
      zoomOnScroll: false, preventScrolling: false, panOnDrag: !touch, zoomOnDoubleClick: true,
    }, h(Background, { gap: 18, size: 1 }), h(Controls, { showInteractive: false, position: 'top-right', orientation: 'horizontal' })))
    render()
    dark.addEventListener('change', render)
  }
}

main()

"""Build rfc-template.html from RFC_TEMPLATE.md so the two never drift apart.

Run from this folder:
    uv run --with markdown python build.py
"""
import html, json, re
from pathlib import Path
import markdown

here = Path(__file__).parent
src = (here / 'RFC_TEMPLATE.md').read_text(encoding='utf-8')

md = markdown.Markdown(extensions=['tables', 'fenced_code', 'sane_lists', 'toc'],
                       extension_configs={'toc': {'toc_depth': '2-3'}})
body = md.convert(src)

# Task lists: "- [ ] item" -> checkbox
body = re.sub(r'<li>\[ \]\s*', '<li class="task"><input type="checkbox"> ', body)
body = re.sub(r'<li>\[x\]\s*', '<li class="task"><input type="checkbox" checked> ', body, flags=re.I)
# Guidance blockquotes get their own style
body = body.replace('<blockquote>', '<blockquote class="guide">')
# Placeholders like {Name} are highlighted so empty fields stand out (not inside code)
parts = re.split(r'(<code>.*?</code>|<pre>.*?</pre>)', body, flags=re.S)
body = ''.join(p if p.startswith(('<code>', '<pre>')) else re.sub(r'\{([^{}\n]{1,160})\}', r'<span class="ph">{\1}</span>', p) for p in parts)

def walk(tokens):
    for t in tokens:
        yield t
        yield from walk(t.get('children', []))
sections = [t for t in walk(md.toc_tokens) if t['level'] == 2]
toc = ''.join(f'<li><a href="#{t["id"]}">{html.escape(t["name"])}</a></li>' for t in sections)

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RFC Template</title>
<meta name="description" content="RFC template for full-stack features: frontend, backend, data, infrastructure, security, event tracking, translations, Datadog monitoring, rollout and approvals.">
<style>
  :root {{
    --bg: #f7f8fa; --paper: #ffffff; --ink: #1f2430; --muted: #5d6475; --line: #e3e6ec;
    --accent: #3b5bdb; --accent-soft: #edf2ff; --guide-bg: #fff8e6; --guide-line: #f0b429;
    --ph: #b4235a; --ph-bg: #fdecf2; --code: #f1f3f7;
    --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    color-scheme: light;
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --bg: #14171d; --paper: #1c2028; --ink: #e8ebf1; --muted: #a3aab9; --line: #2e3440;
      --accent: #8ea8ff; --accent-soft: #232b45; --guide-bg: #2a2416; --guide-line: #c9971f;
      --ph: #ff8fb5; --ph-bg: #3a1f2b; --code: #252a34; color-scheme: dark;
    }}
  }}
  :root[data-theme="dark"] {{ color-scheme: dark; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--ink); font: 15.5px/1.6 var(--sans); }}
  .layout {{ display: grid; grid-template-columns: 260px minmax(0, 1fr); max-width: 1280px; margin: 0 auto; }}
  nav.side {{ position: sticky; top: 0; align-self: start; height: 100vh; overflow-y: auto; padding: 20px 14px 20px 20px; border-right: 1px solid var(--line); }}
  nav.side h2 {{ font-size: .8rem; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); margin: 0 0 8px; }}
  nav.side ol {{ list-style: none; margin: 0; padding: 0; }}
  nav.side a {{ display: block; padding: 4px 8px; border-radius: 6px; color: var(--ink); text-decoration: none; font-size: .9rem; }}
  nav.side a:hover, nav.side a.on {{ background: var(--accent-soft); color: var(--accent); }}
  .actions {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 0 0 16px; }}
  .actions button {{ font: inherit; font-size: .85rem; padding: 6px 10px; border-radius: 8px; border: 1px solid var(--line); background: var(--paper); color: var(--ink); cursor: pointer; }}
  .actions button.primary {{ background: var(--accent); border-color: var(--accent); color: #fff; }}
  main {{ padding: 28px 32px 80px; min-width: 0; }}
  article {{ background: var(--paper); border: 1px solid var(--line); border-radius: 14px; padding: 28px 32px; }}
  h1 {{ font-size: 1.9rem; margin: 0 0 14px; }}
  h2 {{ font-size: 1.3rem; margin: 34px 0 10px; padding-top: 14px; border-top: 1px solid var(--line); scroll-margin-top: 16px; }}
  h3 {{ font-size: 1.05rem; margin: 22px 0 8px; scroll-margin-top: 16px; }}
  p, li {{ margin: 6px 0; }}
  hr {{ border: 0; border-top: 1px solid var(--line); margin: 22px 0; }}
  .table-wrap {{ overflow-x: auto; margin: 10px 0; border: 1px solid var(--line); border-radius: 10px; }}
  table {{ border-collapse: collapse; width: 100%; font-size: .9rem; }}
  th, td {{ text-align: left; vertical-align: top; padding: 8px 10px; border-bottom: 1px solid var(--line); }}
  th {{ background: var(--accent-soft); font-weight: 650; white-space: nowrap; }}
  tr:last-child td {{ border-bottom: 0; }}
  blockquote.guide {{ margin: 10px 0; padding: 8px 14px; background: var(--guide-bg); border-left: 4px solid var(--guide-line); border-radius: 0 8px 8px 0; color: var(--muted); font-size: .92rem; }}
  blockquote.guide p {{ margin: 4px 0; }}
  .hide-guides blockquote.guide {{ display: none; }}
  .ph {{ color: var(--ph); background: var(--ph-bg); border-radius: 4px; padding: 0 3px; font-size: .92em; }}
  code {{ font-family: var(--mono); font-size: .88em; background: var(--code); padding: 1px 5px; border-radius: 5px; }}
  pre {{ background: var(--code); padding: 12px 14px; border-radius: 10px; overflow-x: auto; }}
  pre code {{ background: none; padding: 0; }}
  li.task {{ list-style: none; margin-left: -1.2em; }}
  li.task input {{ width: 16px; height: 16px; margin-right: 6px; vertical-align: -2px; accent-color: var(--accent); }}
  .toast {{ position: fixed; bottom: 18px; left: 50%; transform: translateX(-50%); background: var(--ink); color: var(--bg); padding: 8px 14px; border-radius: 10px; font-size: .9rem; opacity: 0; transition: opacity .2s; pointer-events: none; }}
  .toast.show {{ opacity: 1; }}
  @media (max-width: 900px) {{
    .layout {{ grid-template-columns: 1fr; }}
    nav.side {{ position: static; height: auto; border-right: 0; border-bottom: 1px solid var(--line); padding: 14px 16px; }}
    nav.side ol {{ display: none; }}
    main {{ padding: 16px; }}
    article {{ padding: 18px 16px; }}
  }}
  @media print {{
    nav.side, .actions, .toast {{ display: none !important; }}
    .layout {{ display: block; }} main {{ padding: 0; }} body {{ background: #fff; color: #000; }}
    article {{ border: 0; padding: 0; }} h2 {{ break-after: avoid; }} .table-wrap {{ overflow: visible; }}
  }}
</style>
</head>
<body>
<div class="layout">
  <nav class="side" aria-label="Sections">
    <div class="actions">
      <button class="primary" id="copyMd">Copy Markdown</button>
      <button id="dlMd">Download .md</button>
      <button id="toggleGuides" aria-pressed="false">Hide guidance</button>
      <button id="print">Print / PDF</button>
    </div>
    <h2>Sections</h2>
    <ol>{toc}</ol>
  </nav>
  <main><article id="doc">{body}</article></main>
</div>
<div class="toast" id="toast" role="status"></div>
<script id="md-source" type="application/json">{json.dumps(src).replace("</", "<\\/")}</script>
<script>
(() => {{
  const md = JSON.parse(document.getElementById('md-source').textContent);
  const toast = (m) => {{ const t = document.getElementById('toast'); t.textContent = m; t.classList.add('show'); setTimeout(() => t.classList.remove('show'), 1800); }};
  // Wrap tables so wide ones scroll on small screens
  document.querySelectorAll('#doc table').forEach((t) => {{ const w = document.createElement('div'); w.className = 'table-wrap'; t.replaceWith(w); w.appendChild(t); }});
  document.getElementById('copyMd').addEventListener('click', async () => {{
    try {{ await navigator.clipboard.writeText(md); toast('Markdown copied'); }}
    catch {{ const ta = document.createElement('textarea'); ta.value = md; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove(); toast('Markdown copied'); }}
  }});
  document.getElementById('dlMd').addEventListener('click', () => {{
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([md], {{ type: 'text/markdown' }})); a.download = 'rfc-000-feature-name.md'; a.click();
  }});
  const tg = document.getElementById('toggleGuides');
  tg.addEventListener('click', () => {{ const on = document.body.classList.toggle('hide-guides'); tg.setAttribute('aria-pressed', String(on)); tg.textContent = on ? 'Show guidance' : 'Hide guidance'; }});
  document.getElementById('print').addEventListener('click', () => window.print());
  // Highlight the section in view
  const links = [...document.querySelectorAll('nav.side a')];
  const byId = new Map(links.map((a) => [a.getAttribute('href').slice(1), a]));
  const io = new IntersectionObserver((es) => es.forEach((e) => {{ if (e.isIntersecting) {{ links.forEach((a) => a.classList.remove('on')); byId.get(e.target.id)?.classList.add('on'); }} }}), {{ rootMargin: '0px 0px -75% 0px' }});
  document.querySelectorAll('#doc h2[id]').forEach((h) => io.observe(h));
}})();
</script>
</body>
</html>
'''
(here / 'rfc-template.html').write_text(page, encoding='utf-8')
print(f'wrote rfc-template.html ({len(page):,} bytes, {len(sections)} sections)')

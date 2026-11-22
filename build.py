"""Build the HTML pages from the Markdown sources so they never drift apart.

    uv run --with markdown python build.py

Outputs:
  rfc-template.html            from RFC_TEMPLATE.md
  examples/<name>.html         from examples/rfc-*.md
  index.html                   landing page linking everything

Also checks every example: the required sections are present, and every
section left out is listed in its "Sections not included" row.
"""
import html, json, re, sys
from pathlib import Path
import markdown

HERE = Path(__file__).parent
REQUIRED = {1, 2, 3, 6, 17, 18, 21, 25}
ALL_SECTIONS = set(range(1, 26))

# Supporting workflow documents rendered as styled HTML pages by the same builder.
SUPPORT_DOCS = [
    ("intake/FEATURE_REQUEST_TEMPLATE.md", "Feature intake", "Business-facing request brief"),
    ("guides/WORKFLOW.md", "End-to-end workflow", "Stages, roles, statuses and hand-offs"),
    ("guides/DEFINITION_OF_READY.md", "Definition of Ready", "Feature and story readiness checks"),
    ("guides/DEFINITION_OF_DONE.md", "Definition of Done", "Shared completion and release checks"),
    ("guides/REVIEW_AND_APPROVAL.md", "Review and approval", "Impact-based review and approval matrix"),
    ("guides/ESTIMATION_GUIDELINES.md", "Estimation guidelines", "Team estimates, confidence and planning"),
    ("templates/DELIVERY_PLAN_TEMPLATE.md", "Delivery plan", "Workstreams, deliverables and dependencies"),
    ("templates/JIRA_STORY_TEMPLATE.md", "Jira story template", "Consistent Story and Task descriptions"),
    ("templates/ROVO_WORK_BREAKDOWN_PROMPT.md", "Rovo work breakdown", "Human-reviewed Jira work item prompt"),
    ("examples/CROSS_TEAM_DELIVERY_PLAN.md", "Cross-team example", "Peer Field Intelligence delivery example"),
]

CSS = """
  :root { --bg:#f7f8fa; --paper:#fff; --ink:#1f2430; --muted:#5d6475; --line:#e3e6ec; --accent:#3b5bdb; --accent-soft:#edf2ff;
    --guide-bg:#fff8e6; --guide-line:#f0b429; --ph:#b4235a; --ph-bg:#fdecf2; --code:#f1f3f7;
    --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; color-scheme:light; }
  @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#14171d; --paper:#1c2028; --ink:#e8ebf1; --muted:#a3aab9; --line:#2e3440;
    --accent:#8ea8ff; --accent-soft:#232b45; --guide-bg:#2a2416; --guide-line:#c9971f; --ph:#ff8fb5; --ph-bg:#3a1f2b; --code:#252a34; color-scheme:dark; } }
  :root[data-theme="dark"] { color-scheme:dark; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--ink); font:15.5px/1.6 var(--sans); }
  a { color:var(--accent); }
  .layout { display:grid; grid-template-columns:260px minmax(0,1fr); max-width:1280px; margin:0 auto; }
  nav.side { position:sticky; top:0; align-self:start; height:100vh; overflow-y:auto; padding:20px 14px 20px 20px; border-right:1px solid var(--line); }
  nav.side h2 { font-size:.8rem; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); margin:14px 0 8px; }
  nav.side ol { list-style:none; margin:0; padding:0; }
  nav.side a { display:block; padding:4px 8px; border-radius:6px; color:var(--ink); text-decoration:none; font-size:.9rem; }
  nav.side a:hover, nav.side a.on { background:var(--accent-soft); color:var(--accent); }
  .home { font-size:.9rem; text-decoration:none; }
  .actions { display:flex; flex-wrap:wrap; gap:6px; margin:10px 0 6px; }
  .actions button { font:inherit; font-size:.85rem; padding:6px 10px; border-radius:8px; border:1px solid var(--line); background:var(--paper); color:var(--ink); cursor:pointer; }
  .actions button.primary { background:var(--accent); border-color:var(--accent); color:#fff; }
  main { padding:28px 32px 80px; min-width:0; }
  article { background:var(--paper); border:1px solid var(--line); border-radius:14px; padding:28px 32px; }
  h1 { font-size:1.9rem; margin:0 0 14px; line-height:1.25; }
  h2 { font-size:1.3rem; margin:34px 0 10px; padding-top:14px; border-top:1px solid var(--line); scroll-margin-top:16px; }
  h3 { font-size:1.05rem; margin:22px 0 8px; scroll-margin-top:16px; }
  p, li { margin:6px 0; }
  hr { border:0; border-top:1px solid var(--line); margin:22px 0; }
  .table-wrap { overflow-x:auto; margin:10px 0; border:1px solid var(--line); border-radius:10px; }
  table { border-collapse:collapse; width:100%; font-size:.9rem; }
  th, td { text-align:left; vertical-align:top; padding:8px 10px; border-bottom:1px solid var(--line); }
  th { background:var(--accent-soft); font-weight:650; white-space:nowrap; }
  tr:last-child td { border-bottom:0; }
  blockquote.guide { margin:10px 0; padding:8px 14px; background:var(--guide-bg); border-left:4px solid var(--guide-line); border-radius:0 8px 8px 0; color:var(--muted); font-size:.92rem; }
  blockquote.guide p { margin:4px 0; }
  .hide-guides blockquote.guide { display:none; }
  .ph { color:var(--ph); background:var(--ph-bg); border-radius:4px; padding:0 3px; font-size:.92em; }
  code { font-family:var(--mono); font-size:.88em; background:var(--code); padding:1px 5px; border-radius:5px; }
  pre { background:var(--code); padding:12px 14px; border-radius:10px; overflow-x:auto; }
  pre code { background:none; padding:0; }
  li.task { list-style:none; margin-left:-1.2em; }
  li.task input { width:16px; height:16px; margin-right:6px; vertical-align:-2px; accent-color:var(--accent); }
  .toast { position:fixed; bottom:18px; left:50%; transform:translateX(-50%); background:var(--ink); color:var(--bg); padding:8px 14px; border-radius:10px; font-size:.9rem; opacity:0; transition:opacity .2s; pointer-events:none; }
  .toast.show { opacity:1; }
  .cards { display:grid; gap:14px; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); margin-top:14px; }
  .card { display:block; background:var(--paper); border:1px solid var(--line); border-radius:14px; padding:16px 18px; text-decoration:none; color:var(--ink); }
  .card:hover { border-color:var(--accent); }
  .card .tag { font-size:.75rem; font-weight:700; color:var(--accent); text-transform:uppercase; letter-spacing:.05em; }
  .card h3 { margin:4px 0 6px; font-size:1.05rem; }
  .card p { margin:0; color:var(--muted); font-size:.92rem; }
  .bar { display:flex; gap:2px; margin-top:10px; }
  .bar i { flex:1; height:8px; border-radius:2px; background:var(--line); }
  .bar i.on { background:var(--accent); }
  @media (max-width:900px) { .layout { grid-template-columns:1fr; } nav.side { position:static; height:auto; border-right:0; border-bottom:1px solid var(--line); padding:14px 16px; }
    nav.side ol { display:none; } main { padding:16px; } article { padding:18px 16px; } }
  @media print { nav.side, .actions, .toast { display:none !important; } .layout { display:block; } main { padding:0; } body { background:#fff; color:#000; }
    article { border:0; padding:0; } h2 { break-after:avoid; } .table-wrap { overflow:visible; } }
"""

JS = """
(() => {
  const md = JSON.parse(document.getElementById('md-source').textContent);
  const name = document.body.dataset.download;
  const toast = (m) => { const t = document.getElementById('toast'); t.textContent = m; t.classList.add('show'); setTimeout(() => t.classList.remove('show'), 1800); };
  document.querySelectorAll('#doc table').forEach((t) => { const w = document.createElement('div'); w.className = 'table-wrap'; t.replaceWith(w); w.appendChild(t); });
  document.getElementById('copyMd').addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(md); } catch { const ta = document.createElement('textarea'); ta.value = md; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove(); }
    toast('Markdown copied');
  });
  document.getElementById('dlMd').addEventListener('click', () => { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([md], { type: 'text/markdown' })); a.download = name; a.click(); });
  const tg = document.getElementById('toggleGuides');
  if (tg) tg.addEventListener('click', () => { const on = document.body.classList.toggle('hide-guides'); tg.setAttribute('aria-pressed', String(on)); tg.textContent = on ? 'Show guidance' : 'Hide guidance'; });
  document.getElementById('print').addEventListener('click', () => window.print());
  const links = [...document.querySelectorAll('nav.side ol a')];
  const byId = new Map(links.map((a) => [a.getAttribute('href').slice(1), a]));
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { links.forEach((a) => a.classList.remove('on')); byId.get(e.target.id)?.classList.add('on'); } }), { rootMargin: '0px 0px -75% 0px' });
  document.querySelectorAll('#doc h2[id]').forEach((h) => io.observe(h));
})();
"""


def walk(tokens):
    for t in tokens:
        yield t
        yield from walk(t.get('children', []))


def render(src, *, highlight_placeholders):
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'sane_lists', 'toc'], extension_configs={'toc': {'toc_depth': '2-3'}})
    body = md.convert(src)
    body = re.sub(r'<li>\[ \]\s*', '<li class="task"><input type="checkbox"> ', body)
    body = re.sub(r'<li>\[x\]\s*', '<li class="task"><input type="checkbox" checked> ', body, flags=re.I)
    body = body.replace('<blockquote>', '<blockquote class="guide">')
    if highlight_placeholders:
        parts = re.split(r'(<code>.*?</code>|<pre>.*?</pre>)', body, flags=re.S)
        body = ''.join(p if p.startswith(('<code>', '<pre>')) else re.sub(r'\{([^{}\n]{1,160})\}', r'<span class="ph">{\1}</span>', p) for p in parts)
    sections = [t for t in walk(md.toc_tokens) if t['level'] == 2]
    return body, sections


def page(*, title, src, body, sections, download, home_href, guides_button):
    toc = ''.join(f'<li><a href="#{t["id"]}">{html.escape(t["name"])}</a></li>' for t in sections)
    guides = '<button id="toggleGuides" aria-pressed="false">Hide guidance</button>' if guides_button else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{CSS}</style>
</head>
<body data-download="{html.escape(download)}">
<div class="layout">
  <nav class="side" aria-label="Sections">
    <a class="home" href="{home_href}">← All RFC documents</a>
    <div class="actions">
      <button class="primary" id="copyMd">Copy Markdown</button>
      <button id="dlMd">Download .md</button>
      {guides}
      <button id="print">Print / PDF</button>
    </div>
    <h2>Sections</h2>
    <ol>{toc}</ol>
  </nav>
  <main><article id="doc">{body}</article></main>
</div>
<div class="toast" id="toast" role="status"></div>
<script id="md-source" type="application/json">{json.dumps(src).replace("</", "<\\/")}</script>
<script>{JS}</script>
</body>
</html>
'''


def check_example(path, src):
    present = {int(n) for n in re.findall(r'^## (\d+)\.', src, re.M)}
    row = re.search(r'^\| Sections not included \| (.+?) \|$', src, re.M)
    listed = {int(n) for n in re.findall(r'(?:^|·)\s*(\d{1,2})\s', row.group(1))} if row else set()
    problems = []
    if REQUIRED - present:
        problems.append(f'missing required sections {sorted(REQUIRED - present)}')
    unexplained = (ALL_SECTIONS - present) - listed
    if unexplained:
        problems.append(f'sections left out but not listed in "Sections not included": {sorted(unexplained)}')
    wrongly = listed & present
    if wrongly:
        problems.append(f'sections listed as not included but present: {sorted(wrongly)}')
    return present, problems


def main():
    errors = []
    # template
    src = (HERE / 'RFC_TEMPLATE.md').read_text(encoding='utf-8')
    body, secs = render(src, highlight_placeholders=True)
    (HERE / 'rfc-template.html').write_text(page(title='RFC Template', src=src, body=body, sections=secs,
        download='rfc-000-feature-name.md', home_href='index.html', guides_button=True), encoding='utf-8')
    print(f'rfc-template.html: {len(secs)} sections')
    # examples
    cards = []
    for path in sorted((HERE / 'examples').glob('rfc-*.md')):
        src = path.read_text(encoding='utf-8')
        present, problems = check_example(path, src)
        for p in problems:
            errors.append(f'{path.name}: {p}')
        body, secs = render(src, highlight_placeholders=False)
        out = path.with_suffix('.html')
        title = re.search(r'^# (.+)$', src, re.M).group(1)
        out.write_text(page(title=title, src=src, body=body, sections=secs, download=path.name,
            home_href='../index.html', guides_button=False), encoding='utf-8')
        rid = re.search(r'\| RFC ID \| (RFC-\d+) \|', src).group(1)
        shape = re.search(r'^> Example RFC[^.]*\.\s*(.+)$', src, re.M)
        cards.append((rid, title.replace('RFC: ', ''), f'examples/{out.name}', shape.group(1) if shape else '', present))
        print(f'{out.relative_to(HERE)}: {len(secs)} sections')
    # Supporting workflow documents
    support_cards = []
    for rel_path, label, description in SUPPORT_DOCS:
        path = HERE / rel_path
        src = path.read_text(encoding='utf-8')
        body, secs = render(src, highlight_placeholders=True)
        out = path.with_suffix('.html')
        title_match = re.search(r'^# (.+)
        return '<div class="bar" aria-label="sections used">' + ''.join(f'<i class="{"on" if n in present else ""}" title="Section {n}"></i>' for n in range(1, 26)) + '</div>'
    card_html = ''.join(f'<a class="card" href="{href}"><span class="tag">{rid} · {len(pr)} of 25 sections</span><h3>{html.escape(t)}</h3><p>{html.escape(shape)}</p>{bar(pr)}</a>' for rid, t, href, shape, pr in cards)
    index = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>RFC Template and Examples</title><style>{CSS} main {{ max-width:1100px; margin:0 auto; }}</style></head>
<body><main>
<h1>Feature request-to-delivery toolkit</h1>
<p>Use the feature request-to-delivery workflow to connect business outcomes, product requirements, engineering design, team breakdown and Jira execution. Select the lightest process that safely covers the change.</p>
<h2>Feature workflow toolkit</h2>
<div class="cards">{support_card_html}</div>
<h2>Technical RFC</h2>
<div class="cards"><a class="card" href="rfc-template.html"><span class="tag">Template</span><h3>RFC template</h3><p>Technical requirements, architecture, risk, delivery and operational planning.</p>{bar(ALL_SECTIONS)}</a></div>
<h2>Examples</h2>
<p>Technical RFC examples for a fictional online store. The bars show which of the 25 technical sections each example uses.</p>
<div class="cards">{card_html}</div>
</main></body></html>
'''
    (HERE / 'index.html').write_text(index, encoding='utf-8')
    print('index.html written')
    if errors:
        print('\nCHECK FAILED:\n  - ' + '\n  - '.join(errors))
        sys.exit(1)
    print('all examples pass the section checks')


main()
, src, re.M)
        title = title_match.group(1) if title_match else label
        out.write_text(page(title=title, src=src, body=body, sections=secs,
            download=path.name, home_href='../index.html', guides_button=True), encoding='utf-8')
        href = out.relative_to(HERE).as_posix()
        support_cards.append((href, label, description))
        print(f'{href}: {len(secs)} sections')
    # index
    support_card_html = ''.join(
        f'<a class="card" href="{html.escape(href, quote=True)}"><span class="tag">Workflow resource</span>'
        f'<h3>{html.escape(label)}</h3><p>{html.escape(description)}</p></a>'
        for href, label, description in support_cards
    )

    def bar(present):
        return '<div class="bar" aria-label="sections used">' + ''.join(f'<i class="{"on" if n in present else ""}" title="Section {n}"></i>' for n in range(1, 26)) + '</div>'
    card_html = ''.join(f'<a class="card" href="{href}"><span class="tag">{rid} · {len(pr)} of 25 sections</span><h3>{html.escape(t)}</h3><p>{html.escape(shape)}</p>{bar(pr)}</a>' for rid, t, href, shape, pr in cards)
    index = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>RFC Template and Examples</title><style>{CSS} main {{ max-width:1100px; margin:0 auto; }}</style></head>
<body><main>
<h1>RFC template for full-stack features</h1>
<p>Fill in the template before work starts. Include only the sections a change needs: sections 1, 2, 3, 6, 17, 18, 21 and 25 are always required, and anything left out is listed with a reason.</p>
<div class="cards"><a class="card" href="rfc-template.html"><span class="tag">Template</span><h3>RFC template</h3><p>All 25 sections with guidance, example rows and a launch checklist. Copy or download as Markdown.</p>{bar(ALL_SECTIONS)}</a></div>
<h2>Examples</h2>
<p>Five RFCs for a fictional online store, each using a different set of sections. The bars show which of the 25 sections each one uses.</p>
<div class="cards">{card_html}</div>
</main></body></html>
'''
    (HERE / 'index.html').write_text(index, encoding='utf-8')
    print('index.html written')
    if errors:
        print('\nCHECK FAILED:\n  - ' + '\n  - '.join(errors))
        sys.exit(1)
    print('all examples pass the section checks')


main()

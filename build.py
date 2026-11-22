"""Generate the documentation site from Markdown sources.

Run with:
    uv run --with markdown python build.py

Markdown is the source of truth. The builder creates the RFC page, example pages,
supporting workflow pages and the landing page, then validates the RFC examples.
"""
import html
import json
import re
import sys
from pathlib import Path

import markdown

HERE = Path(__file__).parent
REQUIRED = {1, 2, 3, 6, 17, 18, 21, 25}
ALL_SECTIONS = set(range(1, 26))

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
:root { --bg:#f7f8fa; --paper:#fff; --ink:#1f2430; --muted:#5d6475; --line:#e3e6ec;
  --accent:#3b5bdb; --accent-soft:#edf2ff; --guide-bg:#fff8e6; --guide-line:#f0b429;
  --ph:#b4235a; --ph-bg:#fdecf2; --code:#f1f3f7;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; color-scheme:light; }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { --bg:#14171d; --paper:#1c2028; --ink:#e8ebf1; --muted:#a3aab9;
    --line:#2e3440; --accent:#8ea8ff; --accent-soft:#232b45; --guide-bg:#2a2416;
    --guide-line:#c9971f; --ph:#ff8fb5; --ph-bg:#3a1f2b; --code:#252a34; color-scheme:dark; }
}
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
@media (max-width:900px) {
  .layout { grid-template-columns:1fr; }
  nav.side { position:static; height:auto; border-right:0; border-bottom:1px solid var(--line); padding:14px 16px; }
  nav.side ol { display:none; }
  main { padding:16px; }
  article { padding:18px 16px; }
}
@media print {
  nav.side, .actions, .toast { display:none !important; }
  .layout { display:block; }
  main { padding:0; }
  body { background:#fff; color:#000; }
  article { border:0; padding:0; }
  h2 { break-after:avoid; }
  .table-wrap { overflow:visible; }
}
"""

JS = """
(() => {
  const md = JSON.parse(document.getElementById('md-source').textContent);
  const name = document.body.dataset.download;
  const toast = (message) => {
    const element = document.getElementById('toast');
    element.textContent = message;
    element.classList.add('show');
    setTimeout(() => element.classList.remove('show'), 1800);
  };
  document.querySelectorAll('#doc table').forEach((table) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'table-wrap';
    table.replaceWith(wrapper);
    wrapper.appendChild(table);
  });
  document.getElementById('copyMd').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(md);
    } catch {
      const area = document.createElement('textarea');
      area.value = md;
      document.body.appendChild(area);
      area.select();
      document.execCommand('copy');
      area.remove();
    }
    toast('Markdown copied');
  });
  document.getElementById('dlMd').addEventListener('click', () => {
    const link = document.createElement('a');
    link.href = URL.createObjectURL(new Blob([md], { type: 'text/markdown' }));
    link.download = name;
    link.click();
    URL.revokeObjectURL(link.href);
  });
  const toggle = document.getElementById('toggleGuides');
  if (toggle) toggle.addEventListener('click', () => {
    const hidden = document.body.classList.toggle('hide-guides');
    toggle.setAttribute('aria-pressed', String(hidden));
    toggle.textContent = hidden ? 'Show guidance' : 'Hide guidance';
  });
  document.getElementById('print').addEventListener('click', () => window.print());
  const links = [...document.querySelectorAll('nav.side ol a')];
  const byId = new Map(links.map((link) => [link.getAttribute('href').slice(1), link]));
  const observer = new IntersectionObserver((entries) => entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    links.forEach((link) => link.classList.remove('on'));
    byId.get(entry.target.id)?.classList.add('on');
  }), { rootMargin: '0px 0px -75% 0px' });
  document.querySelectorAll('#doc h2[id]').forEach((heading) => observer.observe(heading));
})();
"""


def walk(tokens):
    for token in tokens:
        yield token
        yield from walk(token.get("children", []))


def render(source, *, highlight_placeholders):
    parser = markdown.Markdown(
        extensions=["tables", "fenced_code", "sane_lists", "toc"],
        extension_configs={"toc": {"toc_depth": "2-3"}},
    )
    body = parser.convert(source)
    body = re.sub(r"<li>\[ \]\s*", '<li class="task"><input type="checkbox"> ', body)
    body = re.sub(r"<li>\[x\]\s*", '<li class="task"><input type="checkbox" checked> ', body, flags=re.I)
    body = body.replace("<blockquote>", '<blockquote class="guide">')
    if highlight_placeholders:
        parts = re.split(r"(<code>.*?</code>|<pre>.*?</pre>)", body, flags=re.S)
        body = "".join(
            part if part.startswith(("<code>", "<pre>")) else
            re.sub(r"\{([^{}\n]{1,160})\}", r'<span class="ph">{\1}</span>', part)
            for part in parts
        )
    sections = [token for token in walk(parser.toc_tokens) if token["level"] == 2]
    return body, sections


def page(*, title, source, body, sections, download, home_href, guides_button):
    toc = "".join(
        f'<li><a href="#{section["id"]}">{html.escape(section["name"])}</a></li>'
        for section in sections
    )
    guides = (
        '<button id="toggleGuides" aria-pressed="false">Hide guidance</button>'
        if guides_button else ""
    )
    source_json = json.dumps(source).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{CSS}</style>
</head>
<body data-download="{html.escape(download, quote=True)}">
<div class="layout">
  <nav class="side" aria-label="Sections">
    <a class="home" href="{home_href}">← All documents</a>
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
<script id="md-source" type="application/json">{source_json}</script>
<script>{JS}</script>
</body>
</html>
"""


def check_example(path, source):
    present = {int(number) for number in re.findall(r"^## (\d+)\.", source, re.M)}
    row = re.search(r"^\| Sections not included \| (.+?) \|$", source, re.M)
    listed = {
        int(number)
        for number in re.findall(r"(?:^|·)\s*(\d{1,2})\s", row.group(1))
    } if row else set()
    problems = []
    if REQUIRED - present:
        problems.append(f"missing required sections {sorted(REQUIRED - present)}")
    unexplained = (ALL_SECTIONS - present) - listed
    if unexplained:
        problems.append(
            f"sections left out but not listed in 'Sections not included': {sorted(unexplained)}"
        )
    wrongly = listed & present
    if wrongly:
        problems.append(f"sections listed as not included but present: {sorted(wrongly)}")
    # Section titles must match the template, so examples cannot drift from it.
    template_titles = dict(re.findall(r"^## (\d+)\. (.+)$", (HERE / "RFC_TEMPLATE.md").read_text(encoding="utf-8"), re.M))
    for number, title in re.findall(r"^## (\d+)\. (.+)$", source, re.M):
        expected = template_titles.get(number)
        if expected and title.strip() != expected.strip():
            problems.append(f"section {number} is titled '{title}' but the template says '{expected}'")
    return present, problems


def section_bar(present):
    cells = []
    for number in sorted(ALL_SECTIONS):
        active = "on" if number in present else ""
        cells.append(f'<i class="{active}" title="Section {number}"></i>')
    return '<div class="bar" aria-label="sections used">' + "".join(cells) + "</div>"


def main():
    errors = []

    # Technical RFC template
    source = (HERE / "RFC_TEMPLATE.md").read_text(encoding="utf-8")
    body, sections = render(source, highlight_placeholders=True)
    (HERE / "rfc-template.html").write_text(
        page(
            title="Technical RFC template", source=source, body=body, sections=sections,
            download="rfc-000-feature-name.md", home_href="index.html", guides_button=True,
        ),
        encoding="utf-8",
    )
    print(f"rfc-template.html: {len(sections)} sections")

    # Worked RFC examples
    example_cards = []
    for path in sorted((HERE / "examples").glob("rfc-*.md")):
        source = path.read_text(encoding="utf-8")
        present, problems = check_example(path, source)
        errors.extend(f"{path.name}: {problem}" for problem in problems)

        body, sections = render(source, highlight_placeholders=False)
        output = path.with_suffix(".html")
        title_match = re.search(r"^# (.+)$", source, re.M)
        if not title_match:
            errors.append(f"{path.name}: missing document title")
            continue
        title = title_match.group(1)
        output.write_text(
            page(
                title=title, source=source, body=body, sections=sections,
                download=path.name, home_href="../index.html", guides_button=False,
            ),
            encoding="utf-8",
        )
        rid_match = re.search(r"^\| RFC ID \| (RFC-\d+) \|$", source, re.M)
        if not rid_match:
            errors.append(f"{path.name}: missing RFC ID")
            continue
        shape_match = re.search(r"^> Example RFC[^.]*\.\s*(.+)$", source, re.M)
        example_cards.append(
            (rid_match.group(1), title.replace("RFC: ", ""), f"examples/{output.name}",
             shape_match.group(1) if shape_match else "", present)
        )
        print(f"{output.relative_to(HERE)}: {len(sections)} sections")

    # Supporting workflow templates and guides
    support_cards = []
    for relative_path, label, description in SUPPORT_DOCS:
        path = HERE / relative_path
        if not path.exists():
            errors.append(f"supporting document is missing: {relative_path}")
            continue
        source = path.read_text(encoding="utf-8")
        body, sections = render(source, highlight_placeholders=True)
        output = path.with_suffix(".html")
        title_match = re.search(r"^# (.+)$", source, re.M)
        title = title_match.group(1) if title_match else label
        output.write_text(
            page(
                title=title, source=source, body=body, sections=sections,
                download=path.name, home_href="../index.html", guides_button=True,
            ),
            encoding="utf-8",
        )
        href = output.relative_to(HERE).as_posix()
        support_cards.append((href, label, description))
        print(f"{href}: {len(sections)} sections")

    support_card_html = "".join(
        f'<a class="card" href="{html.escape(href, quote=True)}">'
        f'<span class="tag">Workflow resource</span><h3>{html.escape(label)}</h3>'
        f'<p>{html.escape(description)}</p></a>'
        for href, label, description in support_cards
    )
    example_card_html = "".join(
        f'<a class="card" href="{html.escape(href, quote=True)}">'
        f'<span class="tag">{html.escape(rid)} · {len(present)} of 25 sections</span>'
        f'<h3>{html.escape(title)}</h3><p>{html.escape(shape)}</p>{section_bar(present)}</a>'
        for rid, title, href, shape, present in example_cards
    )

    index = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Feature request-to-delivery toolkit</title>
<style>{CSS} main {{ max-width:1100px; margin:0 auto; }}</style>
</head>
<body>
<main>
<h1>Feature request-to-delivery toolkit</h1>
<p>Connect business outcomes, product requirements, engineering design, team breakdown and Jira execution. Select the lightest process that safely covers the change.</p>
<h2>Feature workflow toolkit</h2>
<div class="cards">{support_card_html}</div>
<h2>Technical RFC</h2>
<div class="cards">
<a class="card" href="rfc-template.html"><span class="tag">Template</span>
<h3>Technical RFC template</h3><p>Requirements, architecture, risks, delivery and operational planning.</p>
{section_bar(ALL_SECTIONS)}</a>
</div>
<h2>Worked RFC examples</h2>
<p>Technical RFC examples for a fictional online store. The bars show which technical sections each example uses.</p>
<div class="cards">{example_card_html}</div>
</main>
</body>
</html>
"""
    (HERE / "index.html").write_text(index, encoding="utf-8")
    print("index.html written")

    if errors:
        print("\nCHECK FAILED:\n  - " + "\n  - ".join(errors))
        sys.exit(1)
    print("all example RFCs pass the section checks")


if __name__ == "__main__":
    main()

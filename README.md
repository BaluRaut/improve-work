# improve-work

An RFC template for full-stack features, plus five worked examples. Fill in an RFC before work starts so frontend, backend, infrastructure, security, analytics, translations and monitoring are all thought through up front.

**Not every RFC needs every section.** Sections 1, 2, 3, 6, 17, 18, 21 and 25 are required. Include the others only when the change needs them, and list what you left out in the "Sections not included" row with a reason.

| File | What it is |
|---|---|
| [RFC_TEMPLATE.md](RFC_TEMPLATE.md) | The template (source of truth). Copy it per feature as `rfc-{number}-{short-name}.md`. |
| [examples/](examples/) | Five example RFCs, each using a different set of sections (full stack, backend and infra, frontend only, infra only, translations). |
| `index.html`, `rfc-template.html`, `examples/*.html` | The same documents as styled pages with a section sidebar, copy and download buttons, and print to PDF. Open `index.html` in a browser. |
| `build.py` | Regenerates every HTML page from the Markdown and checks each example follows the section rules. |

After editing any Markdown file, rebuild:

```sh
uv run --with markdown python build.py
```

The build fails if an example is missing a required section, or leaves a section out without listing it under "Sections not included".

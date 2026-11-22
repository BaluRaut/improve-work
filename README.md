# improve-work

Templates for planning work before it starts.

| File | What it is |
|---|---|
| `RFC_TEMPLATE.md` | The RFC template (source of truth). Copy it per feature as `rfc-<number>-<short-name>.md`. |
| `rfc-template.html` | The same template as a styled page: section sidebar, tickable checklists, buttons to copy or download the Markdown, hide the guidance, or print to PDF. Open it in any browser. |
| `build.py` | Regenerates the HTML from the Markdown. |

After editing `RFC_TEMPLATE.md`, rebuild the HTML:

```sh
uv run --with markdown python build.py
```

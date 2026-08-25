#!/usr/bin/env python3
"""HX-Wiki-ready HTML renderer for major Markdown documents (ratified 2026-08-25, Q2).

Stdlib-only, deterministic, self-contained single-file HTML (inline CSS, semantic
HTML5) designed to drop into HX-Wiki later: clean headings with anchors, tables,
code blocks, and Mermaid diagrams carried as <pre class="mermaid"> plus the
mermaid.js initializer (source remains visible when offline).

The Markdown file stays the source of truth. Each generated .html stamps the
source path, full sha256, and generation timestamp in a footer AND in an HTML
comment; --check verifies every stamped hash against the current source so drift
is detectable (run after editing Markdown: re-render, never hand-edit HTML).

Usage:
  render.py                      render every path in scripts/wiki/manifest.txt
  render.py FILE.md [FILE.md..]  render specific files
  render.py --check              verify all manifest entries are in sync (exit 1 on drift)
"""
import hashlib, html, os, re, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANIFEST = os.path.join(ROOT, "scripts", "wiki", "manifest.txt")

CSS = """
:root{color-scheme:light dark}
body{font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;line-height:1.55;
max-width:62rem;margin:0 auto;padding:1.5rem 2rem;color:#1a1a1a;background:#fff}
h1,h2,h3,h4,h5,h6{line-height:1.25;margin-top:1.6em}
h1{border-bottom:2px solid #444;padding-bottom:.3em}
h2{border-bottom:1px solid #ccc;padding-bottom:.2em}
code,pre{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.92em}
code{background:#f0f0f0;padding:.1em .3em;border-radius:3px}
pre{background:#f6f8fa;border:1px solid #ddd;border-radius:6px;padding:.8em;overflow-x:auto}
pre code{background:none;padding:0}
table{border-collapse:collapse;margin:1em 0;width:100%}
th,td{border:1px solid #ccc;padding:.35em .6em;text-align:left;vertical-align:top}
th{background:#f0f0f0}
blockquote{border-left:4px solid #bbb;margin:1em 0;padding:.2em 1em;color:#444;background:#fafafa}
a{color:#0645ad}
.doc-meta{color:#666;font-size:.85em;border-bottom:1px dashed #bbb;padding-bottom:.6em;margin-bottom:1.2em}
footer{margin-top:2.5em;border-top:1px solid #ccc;color:#666;font-size:.8em;padding-top:.8em}
pre.mermaid{background:#fff;border:1px dashed #999}
@media (prefers-color-scheme:dark){
body{color:#ddd;background:#111} h1{border-color:#888} h2{border-color:#555}
code{background:#2a2a2a} pre{background:#1b1b1b;border-color:#444}
th{background:#222} th,td{border-color:#555} blockquote{color:#bbb;background:#191919;border-color:#666}
a{color:#6fa8ff} .doc-meta,footer{color:#999}}
""".strip()

MERMAID_SNIPPET = """
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
mermaid.initialize({startOnLoad:true});
</script>
<!-- If this file is viewed offline or the CDN is blocked, Mermaid diagrams appear
     as their source text inside dashed boxes; that source is the authoritative form. -->
"""

def slug(t):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", t.lower())).strip("-")

def inline(t):
    t = html.escape(t, quote=False)
    spans = []
    def keep(m):
        spans.append(m.group(1))
        return f"\x00{len(spans)-1}\x00"
    t = re.sub(r"`([^`]+)`", keep, t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"(?<![\"'>])(https?://[^\s<)]+)", r'<a href="\1">\1</a>', t)
    t = re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{spans[int(m.group(1))]}</code>", t)
    return t

def render_md(text):
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":  # YAML front matter: metadata, not body
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                lines = lines[i + 1:]
                break
    out, i, has_mermaid = [], 0, False
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^```(\S*)\s*$", ln)
        if m:  # fenced code
            lang, buf = m.group(1), []
            i += 1
            while i < len(lines) and not re.match(r"^```\s*$", lines[i]):
                buf.append(lines[i]); i += 1
            i += 1
            code = html.escape("\n".join(buf), quote=False)
            if lang == "mermaid":
                has_mermaid = True
                out.append(f'<pre class="mermaid">{code}</pre>')
            else:
                cls = f' class="language-{lang}"' if lang else ""
                out.append(f"<pre><code{cls}>{code}</code></pre>")
            continue
        if re.match(r"^\s*$", ln):
            i += 1; continue
        if re.match(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$", ln):
            out.append("<hr>"); i += 1; continue
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            lvl, txt = len(m.group(1)), m.group(2).strip()
            out.append(f'<h{lvl} id="{slug(txt)}">{inline(txt)}</h{lvl}>'); i += 1; continue
        if re.match(r"^>", ln):  # blockquote
            buf = []
            while i < len(lines) and re.match(r"^>", lines[i]):
                buf.append(re.sub(r"^>\s?", "", lines[i])); i += 1
            inner = " ".join(x for x in buf if x.strip())
            out.append(f"<blockquote><p>{inline(inner)}</p></blockquote>")
            continue
        if re.match(r"^\s*\|.*\|\s*$", ln) and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):  # pipe table
            def cells(row):
                return [c.strip() for c in row.strip().strip("|").split("|")]
            head = cells(ln); i += 2
            rows = []
            while i < len(lines) and re.match(r"^\s*\|.*\|\s*$", lines[i]):
                rows.append(cells(lines[i])); i += 1
            t = ["<table><thead><tr>"] + [f"<th>{inline(c)}</th>" for c in head] + ["</tr></thead><tbody>"]
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue
        m = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", ln)
        if m:  # list block (nested by indent; wrapped lines join their item)
            items = []
            while i < len(lines):
                mm = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", lines[i])
                if mm:
                    items.append([len(mm.group(1)), mm.group(2)[0].isdigit(), [inline(mm.group(3))]])
                    i += 1; continue
                if items and re.match(r"^\s+\S", lines[i]):
                    items[-1][2].append(inline(lines[i].strip())); i += 1; continue
                break
            html_parts, stack = [], []  # stack of (indent, tag)
            for ind, ordered, parts in items:
                tag = "ol" if ordered else "ul"
                while stack and stack[-1][0] >= ind:
                    html_parts.append(f"</{stack.pop()[1]}>")
                if not stack or stack[-1][0] < ind:
                    html_parts.append(f"<{tag}>"); stack.append((ind, tag))
                html_parts.append(f"<li>{' '.join(parts)}</li>")
            while stack:
                html_parts.append(f"</{stack.pop()[1]}>")
            out.append("".join(html_parts))
            continue
        buf = [ln.strip()]  # paragraph
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,6}\s|>|```|\s*([-*+]|\d+\.)\s|\s*\|.*\||\s*(-{3,}|\*{3,}|_{3,})\s*$)", lines[i]):
            buf.append(lines[i].strip()); i += 1
        out.append(f"<p>{inline(' '.join(buf))}</p>")
    return "\n".join(out), has_mermaid

TEMPLATE = """<!DOCTYPE html>
<!-- Generated from {relpath} (sha256 {digest}) by scripts/wiki/render.py on {stamp}.
     Markdown is the source of truth — edit the .md and re-render; never hand-edit this file. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
<main class="doc">
{body}
</main>
<footer>Source of truth: <code>{relpath}</code> (sha256 <code>{digest}</code>) · rendered {stamp} by <code>scripts/wiki/render.py</code> · HX-ASF-Servers</footer>
{mermaid}
</body>
</html>
"""

def render_file(rel, check_only=False):
    src = os.path.join(ROOT, rel)
    digest = hashlib.sha256(open(src, "rb").read()).hexdigest()
    dst = os.path.splitext(src)[0] + ".html"
    if check_only:
        if not os.path.exists(dst):
            return (rel, "MISSING html")
        m = re.search(r"sha256 ([0-9a-f]{64})", open(dst, encoding="utf-8").read())
        return (rel, "OK" if m and m.group(1) == digest else "DRIFT")
    text = open(src, encoding="utf-8").read()
    body, has_mermaid = render_md(text)
    title_m = re.search(r"^#\s+(.*)$", text, re.M)
    title = title_m.group(1).strip() if title_m else os.path.basename(rel)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    out = TEMPLATE.format(relpath=rel, digest=digest, stamp=stamp, title=html.escape(title),
                          css=CSS, body=body, mermaid=MERMAID_SNIPPET if has_mermaid else "")
    open(dst, "w", encoding="utf-8").write(out)
    return (rel, "rendered")

def main():
    args = [a for a in sys.argv[1:]]
    check = "--check" in args
    args = [a for a in args if a != "--check"]
    paths = args or [l.strip() for l in open(MANIFEST) if l.strip() and not l.startswith("#")]
    rc = 0
    for rel in paths:
        rel = os.path.relpath(os.path.join(ROOT, rel), ROOT) if os.path.isabs(rel) else rel
        try:
            rel2, status = render_file(rel, check)
            print(f"{status:>9}  {rel2}")
            if check and status != "OK":
                rc = 1
        except FileNotFoundError:
            print(f"  MISSING  {rel} (source not found)")
            rc = 1
    return rc

if __name__ == "__main__":
    sys.exit(main())

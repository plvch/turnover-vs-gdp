"""Build index.html for the post, in the plvch design system.
Reuses the CSS + theme-toggle JS from indexes_cost/post/index.html (same shell as the
other essays). Prose is read from DRAFT_v2.md (single source). The 5 figures are lifted
from charts/graphs_codex/ with their CSS scoped under `.gx` so they render exactly as
built and don't fight the post shell.
NB: figures are LIGHT-ONLY for now (graph tokens are scoped/hardcoded under .gx).
Dark-theme adaptation is the tracked TODO (charts/README.md). Run: python3 build_site.py
"""
import re, glob

HERE = __import__("pathlib").Path(__file__).parent
REF = "/Users/mplvch/Documents/claude_projects/indexes_cost/post/index.html"
ref = open(REF).read()
REF_CSS = re.search(r"<style>(.*?)</style>", ref, re.S).group(1)
REF_JS = re.findall(r"<script>(.*?)</script>", ref, re.S)[-1]

TITLE = "The curious structure of German exports"
DESC = ("German business turns over about EUR 9 trillion a year, roughly twice GDP. "
        "But the figure everyone watches, exports, misses an entire economy German "
        "firms run abroad: EUR 3.4tn of turnover, invisible to GDP.")
SLUG = "turnover-vs-gdp"

# ---------- scope the codex graph CSS under .gx ----------
def scope_css(css, scope=".gx"):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    def scope_sel(sel):
        out = []
        for p in (x.strip() for x in sel.split(",") if x.strip()):
            if p == ":root": continue        # drop hardcoded light tokens; inherit post --oi-*
            elif p in ("html", "body"): out.append(f"{scope} body")
            elif p == "*": out.append(f"{scope} *")
            else: out.append(f"{scope} {p}")
        return ", ".join(out)
    res, i, n = [], 0, len(css)
    while i < n:
        at, br = css.find("@media", i), css.find("{", i)
        if br == -1: break
        if at != -1 and at < br:
            mbr = css.find("{", at); depth, j = 1, css.find("{", at) + 1
            while depth and j < n:
                depth += (css[j] == "{") - (css[j] == "}"); j += 1
            res.append(css[at:mbr].strip() + "{" + scope_css(css[mbr+1:j-1], scope) + "}")
            i = j
        else:
            sel, end = css[i:br].strip(), css.find("}", br)
            body = css[br+1:end].strip()
            if sel:
                ss = scope_sel(sel)
                if ss: res.append(ss + "{" + body + "}")
            i = end + 1
    return "\n".join(res)

GRAPH_CSS = scope_css(open(HERE / "charts/graphs_codex/style.css").read())
# Figures inherit the post's themed --oi-* (light + dark). Supply only the extra
# line colours the graphs need, per theme, and flip in-box "white" text to a dark
# fill in dark mode (where navy/forest boxes become light). This is the dark pass.
GRAPH_CSS += """
.gx{margin:0}
.gx .fig-body{overflow-x:auto}
.gx{--oi-brand-soft:#13345f;--oi-brand-line:#2f5790;--oi-brand-2-soft:#245a44;--oi-brand-2-line:#3e7a5f}
[data-theme="dark"] .gx{--oi-brand-soft:#86a3cf;--oi-brand-line:#a6bce0;--oi-brand-2-soft:#7fb79e;--oi-brand-2-line:#94c3ac}
[data-theme="dark"] .gx .white{fill:var(--oi-page-bg)}
[data-theme="dark"] .gx .fig-body{box-shadow:var(--oi-shadow-figure)}
"""

def figure(n):
    html = open(glob.glob(str(HERE / f"charts/graphs_codex/{n:02d}-*.html"))[0]).read()
    return re.search(r'<figure class="fig">.*?</figure>', html, re.S).group(0)

# ---------- parse DRAFT_v2.md ----------
def md_inline(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return t

raw = open(HERE / "DRAFT_v2.md").read()
toks = re.split(r"(?m)^##\s+(.+)$", raw)
sections = [(toks[i].strip(), toks[i + 1]) for i in range(1, len(toks), 2)]

def blocks_of(content):
    blocks = []
    for para in re.split(r"\n\s*\n", content.strip()):
        para = para.strip()
        if not para: continue
        mv = re.match(r"\[VIZ\s*(\d)", para)
        if mv:
            blocks.append(("viz", int(mv.group(1))))
        elif para.startswith("- "):
            items = []
            for li in para.split("\n"):
                if li.strip().startswith("- "): items.append(li.strip()[2:])
                elif items: items[-1] += " " + li.strip()
            blocks.append(("ul", items))
        else:
            blocks.append(("p", " ".join(l.strip() for l in para.split("\n"))))
    return blocks

def rule(num, title):
    return f'<div class="section-rule"><div class="n">§ {num:02d}</div><div class="t">{title}</div></div>'

def render_essay(num, title, blocks):
    out, in_prose, rule_done = ['<section class="essay">'], False, False
    for kind, val in blocks:
        if kind == "p":
            if not in_prose:
                out.append('<div class="col">')
                if not rule_done: out.append(rule(num, title)); rule_done = True
                out.append('<div class="prose">'); in_prose = True
            out.append(f"<p>{md_inline(val)}</p>")
        elif kind == "viz":
            if in_prose: out.append("</div></div>"); in_prose = False
            out.append(f'<div class="gx col-wide">{figure(val)}</div>')
    if in_prose: out.append("</div></div>")
    out.append("</section>")
    return "".join(out)

# ---------- assemble body ----------
essays, methods_html, num = [], "", 0
for title, content in sections:
    blks = blocks_of(content)
    if title.lower().startswith("methods"):
        m = ['<section class="essay"><div class="col"><div class="methods">',
             "<h4>Method &amp; sources</h4>"]
        for kind, val in blks:
            if kind == "p": m.append(f"<p>{md_inline(val)}</p>")
            elif kind == "ul":
                m.append("<ul>" + "".join(f"<li>{md_inline(x)}</li>" for x in val) + "</ul>")
        m.append('<h4 style="margin-top:28px">Disclaimer</h4><p>This is independent '
                 "research commentary, written for general information. It is not "
                 "investment, legal, tax or policy advice. All figures are the author's "
                 "calculations from public statistics, may contain errors, and describe a "
                 "moment in time. Statistical-office and dataset names are used for "
                 "identification only and imply no affiliation or endorsement. The "
                 "underlying tables are public; if you find an error I would rather hear "
                 "about it than not.</p></div></div></section>")
        methods_html = "".join(m)
    else:
        num += 1
        essays.append(render_essay(num, title, blks))

MAST = '''<header class="masthead"><div class="masthead-inner">
  <a class="wordmark" href="https://plvch.com">plvch</a>
  <div class="mh-meta">
    <span class="hide-sm">Note · Germany</span><span>2026</span>
    <span class="theme-toggle">
      <button data-theme-btn="light" class="active" aria-pressed="true">Light</button>
      <button data-theme-btn="dark" aria-pressed="false">Dark</button>
    </span>
  </div>
</div></header>'''

COVER = f'''<section class="cover col">
  <div class="eyebrow brand">Note · Germany</div>
  <h1>{TITLE}</h1>
  <div class="byline">
    <div><div class="k">Author</div><div class="v">plvch</div></div>
    <div><div class="k">Published</div><div class="v">June 2026</div></div>
    <div><div class="k">Reading</div><div class="v">6 min</div></div>
    <div><div class="k">Data</div><div class="v">Destatis · Eurostat · Bundesbank</div></div>
  </div>
</section>'''

ENDMATTER = '''<aside class="end-matter col-wide" aria-label="About and contact">
  <div><h4>About this note</h4><p>Just a blog note. More on <a href="https://plvch.com">plvch.com</a>.</p></div>
  <div><h4>Contact</h4><p>m(at)plvch.com</p><p>Berlin</p></div>
</aside>'''

FOOT = f'''<footer class="essay-foot col-wide">
  <div>© 2026 plvch · <a href="/legal/#impressum">Impressum</a> · <a href="/legal/#datenschutz">Datenschutz</a></div>
  <div>Research note · {TITLE}</div>
  <div>01 / 01</div>
</footer>'''

DOC = f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{TITLE} — plvch</title>
<meta name="description" content="{DESC}"/>
<meta property="og:type" content="article"/>
<meta property="og:title" content="{TITLE}"/>
<meta property="og:description" content="{DESC}"/>
<meta property="og:url" content="https://plvch.com/{SLUG}/"/>
<meta property="og:image" content="https://plvch.com/{SLUG}/assets/thumb.png"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta name="twitter:card" content="summary_large_image"/>
<link rel="stylesheet" href="assets/plvch-tokens.css"/>
<style>{REF_CSS}
/* ---- codex figures, scoped under .gx (light-only; dark = TODO) ---- */
{GRAPH_CSS}</style>
</head>
<body>
{MAST}
<main class="wrap">
{COVER}
{''.join(essays)}
{methods_html}
{ENDMATTER}
{FOOT}
</main>
<script>{REF_JS}</script>
</body>
</html>'''

open(HERE / "index.html", "w").write(DOC)
print(f"wrote index.html ({len(DOC):,} bytes) | {num} sections, "
      f"REF_CSS {len(REF_CSS):,} + GRAPH_CSS {len(GRAPH_CSS):,} chars")

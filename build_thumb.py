"""Social share card (1200x630, OG / LinkedIn / Substack thumb).

Dark plvch surface. Quiet editorial title on the left; on the right, two
area-proportional bubbles comparing domestic turnover with German-controlled
affiliate turnover abroad. Writes thumb.html; render to assets/thumb.png via
headless Chrome.
"""
import math

BG = "#061a35"
SURFACE = "#081f3f"
INK = "#f6f4ef"
INK2 = "#c7ced8"
INK3 = "#8793a5"
RULE = "#1a355e"
FOREST = "#1b4332"
FOREST_2 = "#2f6a50"
OCHRE = "#b08b3a"
OCHRE_2 = "#d1b469"

HOME, ABROAD = 8.49, 3.39
R_HOME = 132
R_ABROAD = round(R_HOME * math.sqrt(ABROAD / HOME))

HTML = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*{{margin:0;box-sizing:border-box}}
body{{background:{BG}}}
.card{{
  width:1200px;height:630px;overflow:hidden;
  background:{BG};color:{INK};font-family:Inter,system-ui,sans-serif;
  padding:50px 62px 42px;display:flex;flex-direction:column;
}}
.top{{display:flex;justify-content:space-between;align-items:center}}
.wm{{font-size:22px;font-weight:700;letter-spacing:-.045em}}
.ey{{font-size:12px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:{INK3}}}
.main{{flex:1;display:grid;grid-template-columns:1.02fr .98fr;gap:44px;align-items:center;padding:20px 0 18px}}
.kicker{{font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:{OCHRE_2};margin-bottom:18px}}
.h{{font-size:48px;font-weight:760;line-height:1.05;letter-spacing:-.03em;max-width:590px}}
.sub{{margin-top:22px;font-size:22px;font-weight:500;line-height:1.32;color:{INK2};max-width:560px}}
.sub strong{{font-weight:700;color:{INK}}}
.sub .accent{{color:{OCHRE_2};font-weight:700}}
.chart{{position:relative;height:420px;display:flex;align-items:center;justify-content:center}}
.chart-title{{position:absolute;top:14px;left:88px;font-size:12px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:{INK3}}}
svg{{width:560px;height:390px;display:block}}
.bubble-label{{font-size:12px;font-weight:800;letter-spacing:.16em;text-transform:uppercase}}
.bubble-value{{font-size:42px;font-weight:800;letter-spacing:-.03em;font-variant-numeric:tabular-nums}}
.bubble-sub{{font-size:14px;font-weight:600}}
.outside{{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}}
.bottom{{display:flex;justify-content:space-between;align-items:center;border-top:1px solid {RULE};padding-top:14px}}
.bottom span{{font-size:13px;color:{INK3};font-weight:600}}
</style>
</head>
<body>
<div class="card">
  <div class="top">
    <div class="wm">plvch</div>
    <div class="ey">Note · Germany</div>
  </div>

  <div class="main">
    <section>
      <div class="kicker">Exports are only the visible part</div>
      <div class="h">The curious structure<br>of German exports</div>
      <div class="sub">German firms turn over <strong>about €9tn</strong> at home and run a <span class="accent">€3.4tn affiliate economy abroad</span> that GDP does not count.</div>
    </section>

    <section class="chart" aria-label="Gross turnover, 2023: domestic turnover EUR 8.5tn and affiliate turnover abroad EUR 3.4tn">
      <div class="chart-title">Gross turnover, 2023</div>
      <svg viewBox="0 0 560 390" role="img" aria-label="Area proportional bubbles: EUR 8.5tn at home and EUR 3.4tn abroad">
        <circle cx="230" cy="198" r="{R_HOME}" fill="{FOREST}" stroke="{FOREST_2}" stroke-width="2"/>
        <text class="bubble-label" x="230" y="158" text-anchor="middle" fill="#d9eadf">On German soil</text>
        <text class="bubble-value" x="230" y="207" text-anchor="middle" fill="{INK}">€8.5tn</text>
        <text class="bubble-sub" x="230" y="233" text-anchor="middle" fill="#bbd0c4">domestic turnover</text>

        <circle cx="430" cy="256" r="{R_ABROAD}" fill="{OCHRE}" stroke="{OCHRE_2}" stroke-width="2"/>
        <text class="bubble-label" x="430" y="226" text-anchor="middle" fill="{BG}">Abroad</text>
        <text class="bubble-value" x="430" y="265" text-anchor="middle" fill="{BG}">€3.4tn</text>
        <text class="bubble-sub" x="430" y="289" text-anchor="middle" fill="#453815">outside GDP</text>

        <text class="outside" x="430" y="366" text-anchor="middle" fill="{INK3}">affiliate turnover abroad</text>
      </svg>
    </section>
  </div>

  <div class="bottom">
    <span>plvch.com</span>
    <span>Destatis · Eurostat · Bundesbank Outward FATS</span>
  </div>
</div>
</body>
</html>'''

open("thumb.html", "w").write(HTML)
print(f"wrote thumb.html | bubble radii home={R_HOME} abroad={R_ABROAD}")

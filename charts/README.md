# Charts — build specs

Five figures for the essay *The curious structure of German exports* (`../DRAFT_v2.md`).
Each `NN-*.md` is a **self-contained build prompt** for one chart: exact data inline,
full source provenance, and the visual spec. Build one at a time from its file.

| # | File | Goes after (DRAFT_v2 §) |
|---|---|---|
| 1 | `01-gross-output-vs-value-added.md` | §The turnover number |
| 2 | `02-turnover-vs-gdp-dynamics.md` | §Why it moves differently |
| 3 | `03-two-economies.md` | §The part outside Germany (after the 3.39tn line) |
| 4 | `04-growth-race.md` | §The part outside Germany (after the growth rates) |
| 5 | `05-firm-anatomy.md` | §The part outside Germany (the car-company para) |

## Output format
Hand-built **inline SVG** (no charting library), in the plvch design system, to be
lifted straight into the post's `index.html`. Reference build pattern:
`../../small-business-concentration/index.html` (the Lorenz `.lc-svg`, bar tables).
viewBox width ~880–920. Tabular-nums for figures. Uppercase letter-spaced axis labels.
Every SVG gets `role="img"` + `aria-label`. Light mode (the post has a dark theme via
tokens; use the `var(--oi-*)` names so both themes work).

## Design tokens (plvch-tokens.css)
| token | hex (light) | use |
|---|---|---|
| `--oi-brand` navy-800 | `#0b2545` | primary series (turnover) |
| `--oi-brand-2` forest-800 | `#1b4332` | secondary series (GDP) |
| `--oi-accent` ochre | `#b08b3a` | the "ghost" / abroad series — the emphasis colour |
| `--oi-ink-1/2/3` | `#0a0f14 / #2a3038 / #5a6470` | text dark→light |
| `--oi-rule` / `--oi-rule-strong` | `#d8d3c4` / `#0a0f14` | gridlines / axis |
| `--oi-surface` / `-sunk` | `#f6f4ef` / `#ecebe4` | figure bg / bar tracks |
| `--oi-highlight` | `#f1e6c4` | abroad box fill (ochre tint) |

**Lighter variants** (for line charts where navy+forest are both too dark to tell
apart): navy-700 `#13345f`, navy-500 `#2f5790`; forest-700 `#245a44`, forest-500
`#3e7a5f`. Fonts: Inter (display/text), JetBrains Mono (mono).
**Lesson from the failed auto-build:** draw the data geometry FIRST (the polylines,
the bars), verify it renders, then add axes/labels/annotations. Do not ship a chart
whose lines/bars are missing.

## Data files (`../data/`)
- `voran_turnover_vs_gdp.csv` — Destatis Umsatzsteuerstatistik Voranmeldungen
  **73311-0001** (taxable turnover STR042) + GDP (FRED **NGDPSAXDCDEQ**, nominal SA).
  Cols: year, turnover_raw_bn, **turnover_adj_bn** (2021 financial-sector break removed),
  gdp_bn, ratio_adj, raw_yoy, **adj_yoy**, gdp_yoy, gap_pp, taxpayers. 2002–2024.
- `fats_abroad_annual.csv` — Eurostat Outward FATS (`fats_out2_r2` 2010–20 +
  `fats_out_activ` 2021–23), geo=DE, nace=B-S_X_O. Cols: year,
  turnover_abroad_eur_bn, employees, us_turnover_eur_bn, us_share_pct. 2010–2023.
  Corroborated by Bundesbank Outward FATS (2023: EUR 3.4tn, 6.7M).
- `gdp_nominal_annual.csv` — FRED NGDPSAXDCDEQ folded to annual EUR bn. 1991–2025.
- Full provenance + caveats: `../SPINE.md`. Working log: `../NOTES.md`.

## Global caveats (apply to any figure that touches them)
- Turnover is **gross output**, ~2× GDP (value added). Never add turnover + GDP, or
  domestic turnover + abroad turnover (they overlap via intra-group sales).
- **2021 turnover break:** a ~EUR 692bn financial-sector reclassification inflates raw
  2021 (+18.3%). Use `turnover_adj_bn` / `adj_yoy` (clean 2021 = +9.7%). NB the
  adjustment slightly lifts 2022 adj_yoy to +16.6 vs raw +15.4 — for display use the
  raw +15.4 for 2022 (it is clean) and the adjusted +9.7 for 2021 only. See chart 02.

## TODO — dark theme (before lifting into the post)
The built figures in `graphs_codex/` are **LIGHT THEME ONLY**. `style.css` mixes ~17
**hardcoded light hexes** (the plvch light token values: `#0a0f14`, `#f6f4ef`,
`#fbfaf6`, `#f1e6c4`, `#ecebe4`, `#d8d3c4`, `#b08b3a`, `#5a6470`, `#fff`, …) with ~15
`var(--oi-*)` refs, and has **no `data-theme` / dark mapping**. The post `index.html`
ships a full light+dark token system, so before scaffolding:
1. Replace the hardcoded light hexes (in `style.css` and inline in the SVGs) with the
   `var(--oi-*)` tokens, so the figures inherit the post theme (e.g. `#0a0f14` →
   `var(--oi-ink-1)`, `#f6f4ef` → `var(--oi-surface)`, `#b08b3a` → `var(--oi-accent)`).
2. Check contrast in dark mode (`data-theme="dark"`): navy/forest fills on a dark
   surface lose contrast — likely need the lighter variants (navy-500 `#2f5790`,
   forest-500 `#3e7a5f`) in dark; verify gridlines, box borders, ochre, white labels.
3. Re-render and QA **both** light and dark before they go in.

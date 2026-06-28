# Figure 4 — The growth race (abroad turnover pulls away)

**Purpose:** index everything to 2010=100 and show that turnover and employment
*abroad* grew faster than every domestic headline (turnover, exports, GDP, jobs) — the
dynamic part of German business sits outside the macro debate.
**Type:** indexed multi-line chart, 2010=100 → 2023.
**Goes:** §"The part outside Germany", after the growth-rate paragraph.

## Data (index, 2010 = 100)
Real year-by-year series (plot full paths):

| year | Abroad turnover | Abroad jobs | Dom. turnover | GDP (nominal) |
|---|---|---|---|---|
| 2010 | 100.0 | 100.0 | 100.0 | 100.0 |
| 2011 | 111.1 | 104.7 | 108.5 | 105.1 |
| 2012 | 115.4 | 108.6 | 109.8 | 107.3 |
| 2013 | 112.4 | 109.9 | 110.0 | 110.0 |
| 2014 | 122.4 | 113.5 | 112.0 | 114.5 |
| 2015 | 130.9 | 119.3 | 114.3 | 118.2 |
| 2016 | 140.1 | 121.9 | 116.2 | 122.2 |
| 2017 | 142.5 | 127.2 | 121.4 | 127.9 |
| 2018 | 150.6 | 130.4 | 126.4 | 131.8 |
| 2019 | 158.5 | 132.2 | 129.2 | 135.8 |
| 2020 | 146.3 | 129.6 | 124.1 | 132.0 |
| 2021 | 162.3 | 132.2 | 136.2 | 140.7 |
| 2022 | 197.0 | 138.5 | 158.7 | 152.6 |
| 2023 | **205.4** | **142.9** | **162.0** | **161.7** |

Two interpolated series (only endpoints exist → straight CAGR line):
- **Goods exports**: 2010=100 → 2023 = **164.1** (€951.9bn → €1,562.0bn, +3.9%/yr).
- **Domestic employment**: 2010=100 → 2023 = **112.0** (41.02M → 45.93M, +0.9%/yr).

## Source & metadata
- Abroad turnover + jobs: `../data/fats_abroad_annual.csv` (Eurostat Outward FATS,
  geo=DE, nace=B-S_X_O); abroad turnover 1651.3→3391.8, employees 4,683,915→6,691,962.
- Dom. turnover: `voran_turnover_vs_gdp.csv` turnover_adj_bn 5241.0→8492.9.
- GDP: `gdp_nominal_annual.csv` 2609.8→4220.8.
- Exports: Destatis foreign trade, goods, 2010 €951.9bn / 2023 €1,562.0bn.
- Dom. employment: Destatis VGR, Erwerbstätige (Inland), 2010 ≈41.0M / 2023 ≈45.9M.
- **NB on GDP:** this is *nominal* GDP (≈+3.8%/yr, index 162). The draft's "GDP roughly
  3 percent" is *real* GDP; for this nominal index use 162. Flag/decide before print.

## Visual spec
- X = 2010→2023; Y = 100–210. Six lines. Emphasis = the two abroad series in ochre:
  Abroad turnover `--oi-accent`, width ~2.8 (the hero line); Abroad jobs `--oi-accent`
  dashed, width ~1.8. Domestic pack in navy/forest/grey: Dom. turnover navy `#13345f`,
  Exports forest `#245a44`, GDP navy dashed `#2f5790`, Dom. jobs `--oi-ink-3` thin.
- Right-edge end-labels, **vertically de-collided** (Exports 164 / Dom.turnover 162 /
  GDP 162 cluster — nudge so they don't overprint; the failed build overlapped them).
- Legend with all six. Gridlines at 100/120/…/200. viewBox ~ `0 0 920 432`. role="img".
- **Draw the polylines first and confirm all six render before labels.**

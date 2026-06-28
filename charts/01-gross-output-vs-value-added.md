# Figure 1 — Gross output vs value added (why turnover ≈ 2× GDP)

**Purpose:** show, visually, why business turnover comes to about twice GDP — because
every sale along a supply chain is counted in full (turnover), while GDP counts only
the margin each step adds. The 2× gap is double-counting, not extra wealth.
**Type:** schematic horizontal stacked-bar diagram. NOT a data series — illustrative.
**Goes:** end of §"The turnover number", on the line about turnover being ~2× GDP.

## Data (illustrative chain — the only invariant: Σsales = 2 × Σmargins)
A four-stage chain, steel → parts → carmaker → dealer. Each stage's bar = its full
sale; the sale splits into `bought-in input` (= the previous stage's sale) + `margin`
(this stage's value added).

| Stage | bought-in input | margin (value added) | full sale (turnover) |
|---|---|---|---|
| Steel & raw materials | 0 | 4 | 4 |
| Parts & components | 4 | 6 | 10 |
| Carmaker · assembly | 10 | 16 | 26 |
| Dealer · retail | 26 | 14 | 40 |
| **Σ** | | **40 = GDP** | **80 = TURNOVER** |

Σ sales 80 = 2 × Σ margins 40. Units are illustrative "€k per car"; adjust freely as
long as the ratio stays 2.0. **Real-world anchor (state in caption):** 2023 German
domestic turnover **€8.49tn** vs GDP **€4.22tn** = **2.01×**.

## Source & metadata
- Anchor figures: domestic turnover = Destatis Umsatzsteuerstatistik (Voranmeldungen)
  **73311-0001**, STR042, 2023, break-adjusted (`../data/voran_turnover_vs_gdp.csv`,
  `turnover_adj_bn` 2023 = 8492.9). GDP = FRED **NGDPSAXDCDEQ**, 2023 = 4220.8
  (`../data/gdp_nominal_annual.csv`).
- The 4-stage numbers are pedagogical, not from data — label the figure "schematic".

## Visual spec
- 4 stage rows, horizontal bars on a shared 0–~45 scale. Each bar = `[input | margin]`:
  input segment in `--oi-surface-sunk` (#ecebe4) with a thin `--oi-rule` outline;
  margin segment in `--oi-accent` ochre. Right-label each bar with "€{sale}k".
- A small legend up top: ochre swatch = "margin (counts in GDP)", grey swatch =
  "bought-in inputs (already counted upstream)".
- Below a divider, two summary bars on their own 0–90 scale:
  `TURNOVER €80k` (full, `--oi-brand` navy) and `GDP €40k` (`--oi-brand-2` forest),
  with a large `= 2×` to the right.
- viewBox ~ `0 0 900 380`. Tabular-nums on all figures. role="img".

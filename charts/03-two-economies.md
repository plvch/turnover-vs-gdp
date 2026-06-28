# Figure 3 — The two economies (and the one nobody counts)

**Purpose:** put German firms' turnover *abroad* (€3.39tn) next to the visible
figures, so the reader sees the "ghost" economy is ~40% of domestic turnover, ~2× goods
exports, and ~80% of GDP — yet enters no headline.
**Type:** horizontal bar chart, 4 bars, 2023.
**Goes:** §"The part outside Germany", right after the 3.39tn / 6.7M sentence.

## Data (exact, €tn, 2023)
| bar | value €tn | role | colour |
|---|---|---|---|
| Domestic turnover — all sales on German soil | **8.49** | visible | navy `--oi-brand` |
| GDP — value added at home | **4.22** | visible | forest `--oi-brand-2` |
| Turnover abroad — German-owned affiliates (FATS) | **3.39** | **ghost** | **ochre `--oi-accent`** |
| Goods exports — what crosses the border | **1.56** | visible | forest `--oi-brand-2` |

Relations to surface: abroad 3.39 = 40% of domestic 8.49; = 2.2× exports 1.56;
= 80% of GDP 4.22 (gross-vs-value, flag in caption).

## Source & metadata
- Domestic turnover: Destatis Umsatzsteuer (Voranmeldungen) 73311-0001, 2023,
  break-adjusted (`../data/voran_turnover_vs_gdp.csv` turnover_adj_bn 2023 = 8492.9).
- GDP: FRED NGDPSAXDCDEQ 2023 = 4220.8 (`../data/gdp_nominal_annual.csv`).
- Turnover abroad: Eurostat Outward FATS `fats_out_activ` 2023, geo=DE, nace=B-S_X_O =
  3391.8 (`../data/fats_abroad_annual.csv`); corroborated by Bundesbank Outward FATS
  (2023, €3.4tn / 6.7M).
- Goods exports: Destatis foreign trade, 2023 = €1,562.0bn (press PD24_044_51).

## Visual spec
- Horizontal bars, shared scale 0–8.5 (€tn), value label at each bar end, plus a
  small VISIBLE / GHOST tag. Order top→bottom as in the table.
- The abroad bar (ochre) is the emphasis: fill `--oi-accent`, plus a dashed
  `--oi-accent` outline or light hatch to read as "ghost". The three visible bars in
  navy/forest. Axis ticks 0/2/4/6/8.
- Caption must include: "Bars are gross turnover except GDP (value added); do not add
  the visible and ghost bars — they overlap via intra-group sales."
- viewBox ~ `0 0 900 300`. Tabular-nums. role="img". **Draw the rects first; verify
  they render (the failed build emitted a labels-only table with no bars).**

# Figure 2 — Turnover swings about twice as hard as GDP

**Purpose:** two lines, year-on-year, showing turnover is ~2× as volatile as GDP and
that the divergences cluster in *price* shocks (2009 oil/trade, 2022 energy), not real
ones (2020 COVID, where the lines converge).
**Type:** two-line time series, 2005–2024, on a zero baseline.
**Goes:** end of §"Why it moves differently".

## Data (exact — plot these)
YoY %, from `../data/voran_turnover_vs_gdp.csv`. Turnover line = `raw_yoy` for all years
**except 2021**, which uses `adj_yoy` (+9.7) to remove the financial-sector break.
GDP line = `gdp_yoy`.

| year | turnover YoY | GDP YoY | | year | turnover YoY | GDP YoY |
|---|---|---|---|---|---|---|
| 2005 | +5.1 | +1.6 | | 2015 | +2.0 | +3.2 |
| 2006 | +7.9 | +4.5 | | 2016 | +1.6 | +3.4 |
| 2007 | +4.4 | +4.9 | | 2017 | +4.5 | +4.6 |
| 2008 | +5.1 | +1.6 | | 2018 | +4.1 | +3.0 |
| 2009 | **−9.5** | −3.6 | | 2019 | +2.2 | +3.0 |
| 2010 | +7.0 | +4.7 | | 2020 | **−3.9** | **−2.8** |
| 2011 | +8.5 | +5.1 | | 2021 | **+9.7** | +6.7 |
| 2012 | +1.1 | +2.1 | | 2022 | **+15.4** | **+8.4** |
| 2013 | +0.2 | +2.5 | | 2023 | +2.0 | +6.0 |
| 2014 | +1.8 | +4.1 | | 2024 | **−3.0** | +2.6 |

Volatility: turnover YoY std ≈ **5.2 pp** vs GDP **2.7 pp** ⇒ ~2× (state in caption).

## Source & metadata
- Turnover: Destatis Umsatzsteuerstatistik (Voranmeldungen) **73311-0001**, taxable
  turnover STR042, 2002–2024.
- GDP: FRED **NGDPSAXDCDEQ** (nominal, seasonally adjusted, annualised).
- 2021 break: ~€692bn financial-sector reclassification; raw 2021 = +18.3 is
  contaminated; use the +9.7 adjusted value (caption note).

## Visual spec
- X = year 2005→2024; Y = −10 to +18, zero line emphasised (`--oi-rule-strong`).
- Turnover line: `#13345f` (navy-700), width ~2.6. GDP line: `#3e7a5f` (forest-500),
  width ~2. (Use the lighter variants so the two lines are distinguishable — the
  800-weight navy/forest read identical.) Small dots at each data point optional.
- Annotate: 2009 "oil & trade, −9.5", 2022 "energy, +15.4", 2020 "COVID — real shock,
  lines converge". Legend: navy = Business turnover, forest = GDP.
- Gridlines at −10/−5/0/+5/+10/+15. viewBox ~ `0 0 920 440`. role="img".
- **Build the two polylines first and confirm they render** before adding annotations.

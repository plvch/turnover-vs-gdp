# Spine of facts — "Turnover vs GDP, and the economy Germany can't see"

Every figure below is computed from a dataset in `data/` (script named) or sourced
to an official press release. Confidence flagged. All EUR, nominal/current prices
unless noted. This is the fact spine the post will be written from.

**Codex adversarial review (2026-06-22):** verdict — spine "broadly supported on the
main turnover/FATS levels"; all four data/*.py scripts re-run clean. Applied fixes:
§C financial-sector break breadth (~EUR 692bn across WZ64/65/66, not ~220bn
insurance); §G income channel (total primary income vs the narrower direct-investment
subset); §F China=CN_X_HK label + US-export comparator flagged for sourcing.
Both open items now sourced (2026-06-22): US goods exports to the US 2023 = EUR 157.9bn
(Destatis); net direct-investment income 2023 = EUR 70.1bn (Bundesbank BoP II.4b,
gross outward-FDI income EUR 158.0bn). **Spine fully sourced — write-ready.**

---

## A. The subject (continuity from the small-business essay)
- The prior essay cited Destatis Umsatzsteuerstatistik (Veranlagungen) 73321-0004,
  2021: **7.2M VAT-registered firms, ~EUR 8.1tn taxable turnover.** [verified:
  73321-0001 gives STR042 2021 = **EUR 8,118.9bn**, taxpayers 7,215,445.]
- That EUR 8.12tn "Lieferungen und Leistungen" crossed EUR 8tn "for the first time,"
  **+19.82% YoY** — the Destatis headline. [verified to the decimal from 73321-0001.]

## B. Domestic turnover vs GDP — the core finding
Sources: turnover = Destatis Umsatzsteuerstatistik; GDP = FRED NGDPSAXDCDEQ
(nominal, SA, EUR, annualised). Both current prices => like-for-like.
- **Level: turnover ~= 2.0x GDP.** Ratio 1.9–2.1 across 2002–2024, remarkably stable.
- **Turnover is ~2x as volatile as GDP, but they're tightly correlated.**
  Voranmeldungen 2005–2024, break-adjusted (`build_voran_series.py`):
  turnover YoY std **5.15pp** vs GDP **2.68pp** = **1.9x**; **beta 1.61**, **corr 0.84**.
- **It amplifies PRICE shocks, not REAL shocks** (the mechanism: turnover = gross
  output, double-counts intermediate transactions; GDP = value added, nets them out):
  - 2009 oil/trade crash: turnover **-9.5%** vs GDP -3.6%.
  - 2022 energy/inflation: turnover **+15.4%** vs GDP +8.4%.
  - 2020 COVID (real/services, little goods-price move): turnover -3.9% vs GDP -2.8%
    — barely diverged. The contrast is the proof.
- **The round-trip:** nominal turnover +9.7% (2021, clean), **+15.4% (2022)**, +2.0%
  (2023), **-3.0% (2024)** — a boom-bust tracking energy prices that GDP rode out
  smoothly. In 2024 turnover FELL while GDP rose.
- **Latest:** 2024 Voranmeldungen turnover -3.0% YoY — confirmed by Destatis press
  ("Umsatzmilliardäre…", 18 Mar 2026): 825 firms >EUR 1bn each booked EUR 3.4tn =
  38.2% of all taxable turnover; total L&L -3.0%.

## C. The 2021 data break (integrity caution — central to the piece)
- Decomposing the 2021 jump by WZ2008 section (73321-0002 / 73311-0002; sections sum
  exactly to the total): **section K (Financial & insurance) "jumped" from ~EUR 88bn
  to ~EUR 801bn (Veranlagungen) / 82->638bn (Voranmeldungen)** — ~half the entire
  +19.82% rise. The break is **broad across the whole financial sector, not just
  insurance**: WZ64 banks/holdings +164bn (60->224), WZ65 insurance +310bn (5->315),
  WZ66 auxiliary +239bn (24->263). It surfaces as **~EUR 692bn of newly-captured
  tax-exempt-without-deduction turnover** (STR050 inside K: 2.6->694.3bn) — financial
  services are VAT-exempt, so this is a **coverage/Organschaft reclassification of
  financial-sector exempt turnover, not growth.** [verified vs 73321-0002; corrects
  an earlier "~220bn insurance" attribution.]
- A scan of all 18 sections x 13 years: **K-2021 is the ONLY artificial break.**
  (2022's energy +44%, agriculture +46%, hospitality +51% are REAL.)
- Reverting K to trend: **headline +19.82% -> clean ~+9.3–9.9%.** The Destatis press
  release and the prior essay quote the raw figure at face value -> the spectacular
  number is half a mirage. [confidence: high — reproduced in both statistics.]

## D. What the turnover actually is (composition, clean 2020, 73321-0001)
- 70% domestic VAT-charged (STR043, EUR 4,741bn); **18% exports** (STR047, EUR
  1,248bn = EU 659 + non-EU 589); 7% domestic exempt (STR050, EUR 447bn).
- The EUR 1.25tn export slice **cross-checks Germany's known goods exports** -> data sound.

## E. Export-intensity nuance
- Exports look like only ~18% of gross turnover, but that UNDERSTATES exposure
  (gross denominator double-counts domestic B2B; goods-only). Proper metric =
  exports/GDP (Exportquote) **~45–48%**. Goods exports 2023 = **EUR 1,562.0bn**
  (Destatis press PD24_044_51, Feb 2024). Gross turnover makes DE look ~80% domestic;
  value-added shows ~half its net output rides on foreign demand.

## F. The parallel economy abroad — Outward FATS
Sources: Eurostat `fats_out2_r2` (2010–2020) + `fats_out_activ` (2021–2023),
geo=DE controlling, nace=B-S_X_O business economy, indic=turnover; corroborated by
Bundesbank Outward FATS press. Build: `build_fats_series.py`.
- **2023: EUR 3.39tn turnover, 6.69M employees** (Eurostat) — matches Bundesbank's
  **EUR 3.4tn / 6.7M** headline (2023). Independent two-source agreement.
- **Progression:** 1.65tn (2010) -> 2.62tn (2019) -> 2.42 (2020, COVID -7.7%) ->
  3.25 (2022, **+21.4%** energy surge) -> 3.39tn (2023).
- **Growth p.a. (2010–23):** turnover **+5.7%/yr**, headcount **+2.8%/yr**
  (4.7M->6.7M). Both outpaced home (domestic turnover +3.8%/yr, employment +0.9%/yr).
- **Top host countries 2023:** US EUR 760bn (22%), UK 354 (10%), China 278 (8%;
  Eurostat code CN_X_HK = China excl. Hong Kong), France 170 (5%), Switzerland 141
  (4%); Italy 122, Poland 113, Spain 112. (Russia collapsed 37->16bn on sanctions/exit.)
- **Build-in-America >> export-to-America:** German-owned US operations book
  **EUR 760bn** vs German goods exports TO the US **EUR 157.9bn** (Destatis
  PD24_N053_51_42, 2024; US = #1 market, 9.9% of exports) => **4.81x**.
- **Size of the parallel economy:** abroad turnover = ~**40% of domestic turnover**
  (8.5tn) / ~**2.2x goods exports** / ~80% of GDP (gross-vs-net, see caveats).
- **Per head:** gross turnover/head abroad EUR ~507k (2023) vs home ~EUR 185k — ~2.7x,
  but driven by sector mix + double-counting, NOT productivity (caveat below).

## G. What comes back (income) — "Germany books only the dividend"
- **GDP impact: zero by construction** — affiliate output is in HOST-country GDP.
- What returns is *factor income*, not the turnover. The affiliate-specific channel =
  **direct-investment income** (Bundesbank BoP table II.4b, 2023): German residents
  earned **EUR 158.0bn** on outward FDI — of which **EUR 99.0bn distributed (dividends),
  EUR 34.8bn reinvested ABROAD** (never repatriated), rest interest. Net of the
  EUR 87.9bn foreigners earned on inward FDI => **net direct-investment income =
  EUR 70.1bn (2023)**. So profit on the EUR 3.4tn affiliate economy is **<5% of its
  turnover**; the net national-income contribution (~EUR 70bn) is **~1.7% of GDP**.
- For context, the BROADER total primary-income balance was ~EUR 134bn (2023; press
  framed it ~3.5% of GDP) — but that also folds in PORTFOLIO income on Germany's
  passive foreign holdings + labour, NOT just affiliates. **Exports are NOT in primary
  income at all** (goods/trade balance). (GNI 2023 EUR 4,356bn, Destatis; CA surplus
  2023 EUR 280.3bn, Bundesbank.) [corrects an earlier loose "~145bn = affiliate return"
  — 145bn is the broad balance; the affiliate-only net figure is ~70bn.]

## H. Caveats & method (must survive review)
1. **Gross vs value-added** — turnover (gross output) is NOT GDP (value added); the
   ~2x ratio and all "X% of GDP" framings mix the two. Apples-to-apples: abroad
   turnover = 40% of home turnover; in value-added terms the parallel economy is
   est. ~EUR 1.3–1.7tn ~= 30–40% of GDP (FATS value-added not in pulled indic set).
2. **2021 insurance break** — must be flagged wherever 2021 turnover appears.
3. **FATS conventions** — turnover is gross (comparable to domestic); counts the
   affiliate's FULL turnover (control >50%, not ownership share); partially OVERLAPS
   domestic turnover via intra-group sales (don't naively add 8.5 + 3.4).
4. **GDP vintage** — FRED SA-summed (~EUR 4.22tn, 2023) runs above Destatis official
   (~EUR 4.1–4.2tn); use one source per ratio; never mix.
5. **Veranlagungen (7.2M filers, to 2021) vs Voranmeldungen (3.1M filers, to 2024)**
   differ in base/coverage; Voranmeldungen is the primary dynamics series.

## References
- Destatis Umsatzsteuerstatistik (Veranlagungen) 73321-0001/0002 — turnover 2006–21.
- Destatis Umsatzsteuerstatistik (Voranmeldungen) 73311-0001/0002 — turnover 2002–24;
  press "Umsatzmilliardäre…", 18 Mar 2026 (2024 figures, -3.0%).
- FRED NGDPSAXDCDEQ — nominal GDP, SA, quarterly, EUR.
- Destatis foreign trade PD24_044_51 (Feb 2024) — goods exports 2023 = EUR 1,562.0bn.
- Eurostat `fats_out2_r2` (2010–20) + `fats_out_activ` (2021–23) — outward FATS, geo=DE.
- Deutsche Bundesbank — Outward FATS / "Internationale Kapitalverflechtung"; 2023
  EUR 3.4tn / 6.7M / US 22%.
- Deutsche Bundesbank — *Die deutsche Zahlungsbilanz für das Jahr 2023* (primary
  income ~3.5% of GDP; CA surplus EUR 280.3bn).
- Destatis VGR lrvgr04 — Bruttonationaleinkommen (GNI) by year.
- Destatis foreign trade by partner country (PD24_N053_51_42, 2024) — German goods
  exports to the US 2023 = EUR 157.9bn (US = #1 market, 9.9% of exports).
- Bundesbank balance of payments, table II.4b "Erträge aus Direktinvestitionen"
  (Zahlungsbilanzstatistik, 11.06.2026) — 2023: outward-FDI income credits EUR 158.0bn
  (distributed 99.0 / reinvested abroad 34.8), debits EUR 87.9bn, net DI income EUR 70.1bn.

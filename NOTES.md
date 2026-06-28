# Turnover vs GDP — research notes

Working title repo: `turnover-vs-gdp` (slug provisional). Follows the
small-business-concentration essay, which cited Destatis Umsatzsteuerstatistik
(Veranlagungen) 73321-0004, 2021 — 7.2M businesses, EUR 8.1tn taxable turnover.

## The question
Compare the dynamics of German taxable business turnover with nominal GDP.
Hunch: the two are correlated, but turnover is far more *dynamic* than GDP.
Verdict: confirmed, and the divergence is concentrated in price shocks.

## Data
- **Turnover** — Destatis Umsatzsteuerstatistik (Veranlagungen), GENESIS table
  `73321-0001` (Germany total, by year), English flat CSV. Years **2006–2021**.
  Headline metric = `STR042` "Taxable turnover: supplies and services"
  (steuerbarer Umsatz aus Lieferungen und Leistungen). 2021 = EUR 8,118.9bn,
  which reproduces the Destatis headline (8.12tn, +19.82% YoY) exactly, and ties
  to the prior essay. Alt = `STR041` "Taxable turnover" (total, incl.
  intra-Community acquisitions + S.13b). `STR040` = taxpayer count (7.2M in 2021).
  Sector breakdown for the "why": `73321-0002` (4-digit WZ2008, ~308k rows).
- **GDP** — FRED `NGDPSAXDCDEQ`: nominal GDP, seasonally adjusted, EUR millions,
  quarterly. Annual = sum of 4 SA quarters. Both series are *nominal / current
  prices*, so the comparison is like-for-like.
- Scripts: `data/aggregate_gdp.py`, `data/build_series.py`.
  Output: `data/turnover_vs_gdp_annual.csv`.

## !! Data break: the 2021 +19.82% is HALF an artifact
Decomposing the 2021 jump by WZ2008 section (`73321-0002`, sections sum exactly
to the Germany total) exposed a break:
- **Section K (Financial & insurance)** sat at EUR 62-88bn every year 2009-2020,
  then "jumped" to **EUR 801bn in 2021** (+811%, +713bn) = **53% of the entire
  +1,343bn increase**. Source inside K: **insurance** (Non-life 2.4->161bn, Life
  0.5->63bn). Insurance turnover is VAT-*exempt*; 2021 brought ~220bn of
  previously-uncaptured exempt insurance turnover into the statistic. Coverage/
  definition change, not growth (Organschaft/insurance reporting).
- A scan of all 18 sections x 13 years finds **K-2021 is the ONLY anomalous jump**
  in the series. Everything else (incl. the real 2009 oil crash) is clean.
- Reverting K to its 2020 level: **headline +19.82% -> break-adjusted +9.29%**.
  The Destatis press release and the small-business essay both quote the raw
  +19.82% / 8.12tn at face value -> the spectacular figure is half a mirage.

## Key findings (2006–2021, nominal YoY) — BREAK-ADJUSTED
- Turnover level ~= **2.0x GDP**, and the ratio is REMARKABLY STABLE: 1.97-2.15
  (adjusted). The raw "2.21 spike in 2021" is the artifact; clean it's **2.02**,
  in line with every other year. So the ratio is *not* a dramatic price gauge —
  only mild upticks in commodity booms (2008: 2.15, 2011: 2.13).
- Turnover is genuinely more volatile, but **modestly**:
  - std: turnover **4.35pp** vs GDP **2.69pp** => **1.6x** (raw, w/ artifact: 2.2x)
  - YoY range: **18.0pp** (-8.8%..+9.3%) vs GDP 10.3pp => 1.75x
  - **beta 1.43**, correlation **0.89** (corr rises once the break is removed).
- The one clean, large divergence is the **2009 oil/trade crash**: turnover
  **-8.8%** vs GDP -3.6% (gross output amplifies the commodity-price collapse).
- 2020 COVID (real/services, little goods-price move): turnover -3.4% vs GDP
  -2.8% — barely amplified. Consistent with "turnover amplifies PRICE not REAL".
- Mechanism (real part): turnover = **gross output**, double-counts intermediate
  transactions, so commodity/energy price swings compound at every supply-chain
  stage; value-added GDP nets them out. Amplification is ~1.4x, not 2-3x.

## What the turnover actually is (composition, clean year 2020)
steuerbarer Umsatz L&L = 6,776bn, splits into:
- **70% domestic taxed** (STR043, 4,741bn) — VAT-charged sales inside Germany.
- **~18% exports** (STR047, 1,248bn) — zero-rated/exempt-with-deduction: EU
  659bn + non-EU 589bn. **Cross-checks against Germany's known ~1.2tn goods
  exports for 2020** -> the data is sound, and German-produced exports ARE in here.
- **~7% domestic exempt** (STR050, 447bn) — finance/insurance/health/rent.
Confirms the 2021 break: STR050 jumped 447->1,171bn (+724bn) = the insurance
reclassification (matches the +713bn section-K break).

Concept: this is a **territory + gross** measure — sales by businesses operating
in Germany incl. their exports, double-counted across supply-chain layers. NOT
global ownership: VW's US/Mexico/China production-and-sale is in those countries'
stats, not here. turnover/GDP ~= 2.0 = supply-chain length, not net "power".

## Voranmeldungen extension (73311-0001/-0002, 2002–2024) — the real story
Voranmeldungen = advance-VAT-return statistic, EVAS **73311** (NB: 73421 = beer).
~3.1M filers (excludes <22k turnover + near-exempt firms), so a smaller, larger-
firm base than Veranlagungen's 7.2M; total turnover slightly lower (2021: Voran
7.69tn vs Veranl 8.12tn). Better series: 2002–2024, timely, captures the whole
energy round-trip. Headline STR042; GDP merge in `data/build_voran_series.py`,
output `data/voran_turnover_vs_gdp.csv`.
- **2021 insurance break is in BOTH statistics**: Voran section K 82->638bn
  (+677%, 47% of the 2021 rise). Treated as a permanent +556bn step (subtracted
  2021 onward). Clean 2021 = +9.7% (raw +18.3%).
- **2022 = the clean evidence the 2021 break hid.** No artifact (K +7.7%), driven
  by energy/commodity passthrough: **Electricity&gas (D) +44%**, Agriculture +46%,
  Wholesale (G) +14%, Manufacturing (C) +15%, hospitality reopening (I) +51%.
  Turnover **+15.4%** vs GDP +8.4%.
- **The round-trip:** turnover +9.7% (21), +15.4% (22), +2.0% (23), **-3.0% (24)**
  — a nominal boom-bust tracking energy prices. GDP over 23-24: +6.0%, +2.6%.
  In 2024 turnover FELL while GDP grew (gap -5.8pp). 2009 oil crash: -9.5% vs -3.6%.
- Break-scan: only 2021-K is artificial; the 2022 D/A/I jumps are REAL (commodity/
  reopening) — i.e. the volatile sectors are exactly energy/ag/wholesale/hospitality.
- **Amplitude (adj, 2005–2024, n=22):** turnover YoY std **5.15** vs GDP 2.68 =>
  **1.9x**; range 26.1pp vs 12.1pp; **beta 1.61**, corr 0.84. Ratio stable
  **1.89–2.09**, mild peaks in price booms (2008, 2011, 2022). Hunch confirmed:
  turnover ~2x as volatile, amplifies price not real shocks.

## Export share intuition (the "only ~1/5 export" read)
Goods exports = ~18% of gross turnover (STR047). But that UNDERSTATES export
exposure, for two reasons tied to the chain-length theme:
- denominator is gross (turnover ~2x GDP, padded by domestic B2B double-counting);
- it's goods-only — service exports (~0.35tn) are out-of-scope of German VAT.
Proper metric = exports/GDP (Exportquote) ~ **45–48%** (2020 ~45%, 2022 ~48%).
Gross turnover makes DE look ~80% domestic; value-added reveals ~half its NET
output rides on foreign demand. (TiVA domestic-VA-in-exports ~30-35% of GDP — the
"true" dependence after stripping imported input content.) Good sidebar.

## Outward FATS — German firms' turnover ABROAD (the VW-in-US answer)
Source: **Deutsche Bundesbank**, "Auslandsunternehmenseinheiten deutscher
Investoren (Outward FATS)" — turnover/employees/units of foreign affiliates
*controlled by German parents*, by host country & sector. Published annually in
November. Machine-readable mirror: **Eurostat `fats_out2_r2`** (set controlling
country = DE).
- Landing: bundesbank.de .../outward-fats--768894 ; press writeup
  "Internationale Kapitalverflechtung der deutschen Wirtschaft" (615508).
- **2023: EUR 3.4tn turnover, 6.7M employees.** Host split of turnover: EU 36%,
  **US 22% (~EUR 750bn)**, UK 10%, China 8%.
- Trajectory: 1.4tn (2006) -> 1.8tn (2011, 4.9M empl, >26k firms) -> 3.4tn (2023).
- **Full progression** (Eurostat `fats_out2_r2`, NACE Rev.2 vintage 2010-2020,
  geo=DE controlling, partner=WORLD, indic=TUR, nace=B-S_X_O business-economy
  total; extract in `data/extract_fats.py` -> `data/fats_de_extract.csv`):
  2010 1.65 / 2012 1.91 / 2014 2.02 / 2016 2.31 / 2018 2.49 / 2019 **2.62** /
  2020 **2.42** (COVID -7.7%) tn; +Bundesbank 2023 **3.4tn**. ~steady +5-7%/yr.
- **US slice**: stable ~19-23% of abroad-turnover; US-booked turnover 0.30tn
  (2010) -> 0.55tn (2019). vs German goods EXPORTS to the US ~0.11-0.16tn ->
  German-owned US OPERATIONS book ~4-5x what Germany exports TO the US.
- **Auto slice** (C29_C30, 2018): German car-makers' affiliates turned over
  0.37tn abroad, 0.086tn in the US alone (VW Chattanooga / BMW Spartanburg /
  Mercedes Tuscaloosa) — still multiples of German auto exports to the US.
- Eurostat (2010-2020) and Bundesbank (2023) are different vintages but consistent
  in magnitude; the 2020->2023 jump (2.42->3.4) implies a strong energy-era rise.
  560MB source NOT committed; small DE extract kept instead.
- **Top host countries (2019, turnover abroad):** US 0.55tn (21%), UK 0.27 (10%),
  China 0.19 (7%), France 0.15 (6%), Switzerland 0.11 (4%), Italy 0.11, Spain 0.09,
  Austria 0.08. US is #1 by 2x; China #3.
- **Employment abroad:** 4.7M (2010) -> 6.2M (2019) -> 6.1M (2020) -> 6.7M (2023, BBk).
  ~13% of German-controlled-firm employment is now offshore.
- **Gross turnover per head: abroad ~EUR 420-500k vs home ~EUR 150-185k (2.7x).**
  2019: abroad 2.62tn/6.19M = 423k; home 6.77tn(domestic turnover)/45.3M empl = 149k;
  home GDP/head ~78k. CAVEAT: gross turnover/head != productivity — abroad mix is
  selected for high-turnover activities (big mfg + wholesale/distribution) and gross
  double-counts; home denominator includes ~5M public sector with little VAT turnover.
  Real productivity contrast needs value-added (not in this indic set).
- **Series now complete to 2023** via Eurostat `fats_out_activ` (2021-2023; partner
  WRL_REST = world = INT_EU+EXT_EU, verified). Unified: `data/build_fats_series.py`
  -> `data/fats_abroad_annual.csv`. 2021 2.68 / 2022 **3.25 (+21.4%)** / 2023 3.39tn
  — matches Bundesbank 3.4tn. The 2022 energy surge hit turnover ABROAD even harder
  than at home (+21% vs +15%). US: 550->649->760bn (2021-23), ~21% share throughout.
- **Top hosts 2023 (turnover):** US 760bn (22%), UK 354 (10%), China 278 (8%),
  France 170 (5%), Switzerland 141 (4%), Italy 122, Poland 113, Spain 112. Top-5
  same as 2019. Russia collapsed 37->27->16bn (sanctions/exit).
- **Per head:** abroad 423k (2019) / 507k (2023); home turnover/head 150k/185k;
  home GDP/head 78k/92k -> abroad gross turnover/head ~**2.7-2.8x** home (caveat above).
- **Killer stat for the VW intuition:** German-owned US operations book ~EUR 750bn
  turnover vs only ~EUR 157bn of German goods *exports* to the US -> the
  build-in-America channel is ~5x the export-to-America channel. Most of "German
  industry in the US" is local production, invisible to the Umsatzsteuer 8tn.
- Caveats: FATS turnover is gross (same kind as domestic turnover, so comparable),
  counts the affiliate's FULL turnover (control = >50%, not ownership share), and
  partially OVERLAPS domestic turnover via intra-group sales (don't naively add).
- Ladder: Umsatzsteuer ~8tn (German soil) + Outward-FATS 3.4tn (abroad) ~= German
  firms' gross footprint; vs GDP 4.2tn (net value created at home). Foreign
  affiliates alone turn over ~0.8x German GDP.

## Post framing — the payoff section ("ghostly but load-bearing")
The €3.4tn abroad barely touches German GDP or treasuries (cash returning ~= the
thin distributed-dividend slice of ~€100bn DI income; most is reinvested-abroad,
never repatriated). Yet it is **load-bearing for domestic high-value jobs**:
- ACTIVE channel (the real subsidy): foreign affiliates are CUSTOMERS of the German
  parent — buy components/engines/platforms/IP/HQ services; and the foreign volume
  lets German R&D + platform design AMORTISE. So foreign scale underwrites German
  engineering/design/HQ ("brain") jobs precisely by siting production ("hands")
  abroad. Shows up partly as intra-group exports + royalty/service income.
- PASSIVE channel: consolidated earnings -> share price, cost of capital, market
  access, strategic scale. Real but diffuse; doesn't write paychecks.
- VW 2024 is the empirical anchor: China-profit collapse -> immediate German plant-
  closure threats + wage fight. The decisive number (foreign profitability) is
  essentially INVISIBLE to German national accounts.
- Thesis tie: the statistics measure the wrong economy — GDP/turnover see the export
  champion + domestic base, blind to the €3.4tn abroad that increasingly decides
  whether the domestic base survives.
- HONESTY: this is an argued interpretation (VW case + intra-group mechanism), not a
  computed stat. Evidence it; do NOT fabricate "X engineering jobs supported."
- MECHANISM (the sharper close): it's **captive offshoring**, not outsourcing — the
  hands stay INSIDE the firm, so IP/coordination/component demand keep flowing to the
  German brain. The firm offshored the labour, not the value chain. National accounts
  are territorial but the firm is not: German books see the brain + intra-group
  component exports; FATS sees the foreign hands; NEITHER sees the integrated machine.
  Connective tissue = **intra-firm trade** (~1/3 of world trade) — the foreign hands
  appear in German turnover ONLY as the components/IP the parent ships them ("implied
  part of turnover"). Export figure and FATS figure = two ends of the same intra-firm
  pipe; you can't see the pipe from either end. So the real close isn't "the foreign
  economy is invisible" but "the INTEGRATION is invisible, by construction."
  [HONESTY: ~1/3 intra-firm-trade is a global-literature figure; flag as such, don't
  present a Germany-specific intra-group export share we haven't sourced.]

## Status (post-Codex review, 2026-06-22)
Codex review RAN but hung at FINALIZATION both attempts (runtime flaky). Findings
salvaged from the job log + independently verified vs the data. Verdict: spine
"broadly supported on the main turnover/FATS levels"; all 4 data/*.py re-run clean.
APPLIED to SPINE.md:
- §C: 2021 break = ~EUR 692bn FINANCIAL-SECTOR reclassification (WZ64 banks +164 /
  WZ65 insurance +310 / WZ66 auxiliary +239; STR050 inside K 2.6->694bn) — NOT
  "~220bn insurance" as before. [verified vs 73321-0002]
- §G: separated total primary income (~145bn / 3.5% GDP, incl. PORTFOLIO income on
  passive foreign holdings) from the affiliate-only direct-investment-income subset.
  Exports are NOT in primary income (goods/trade balance). CA 2023: goods ~+210 /
  services ~-5 / primary income ~+145 / secondary ~-75 = +280bn.
- §F: China labelled CN_X_HK; US-export comparator flagged; review-provenance note.

SOURCED (2026-06-22) — spine FULLY SOURCED, write-ready:
1. Net direct-investment income 2023 = **EUR 70.1bn** (Bundesbank BoP table II.4b:
   outward-FDI income credits 158.0bn [distributed 99.0 / reinvested abroad 34.8],
   debits 87.9bn). Affiliate profit = <5% of the 3.4tn turnover; net ~1.7% of GDP.
   This is the precise "ghostly but load-bearing" anchor; corrects earlier loose 145bn
   (which is the BROAD primary-income balance incl. portfolio income).
2. German goods exports to the US 2023 = **EUR 157.9bn** (Destatis PD24_N053_51_42;
   US = #1 market). => US affiliate turnover 760bn / 157.9bn = 4.81x build-vs-export.

## Open / next
- DONE — **scaffold** (`index.html` via `build_site.py`, plvch shell, prose from
  DRAFT_v2, 5 figures, methods, thumb/og). Title = "The curious structure of German exports".
- DONE — **dark-theme figures (at post level).** build_site.py drops the `.gx`
  light-token override so figures inherit the post's themed `--oi-*`, supplies per-theme
  line colours, and flips in-box "white" text to a dark fill in dark mode. Verified
  light + dark. NB the standalone `graphs_codex/*.html` are still light-only; the post
  build does the theming.
- DONE — **prose text-style polish** (DRAFT_v2.md): fixed the garbled sentences, rhythm,
  consistent number style; kept the plain voice + decoupling / job-vs-capital points.
- DONE — **thumb** (`build_thumb.py` -> `thumb.html` + `assets/thumb.png`): title + two
  turnover bubbles (home €8.5tn / abroad €3.4tn, ghost). Wired as og:image.
- **NEXT: wire into the blog** — add slug/title/dek to `plvch-blog/build.py` POSTS,
  rebuild. Optional polish: read the full essay end-to-end once in the browser.
- **Gap:** Veranlagungen 73321 ends at **2021**. The 2022 energy peak (nominal GDP
  +8.4%) is not in this table yet; turnover almost certainly spiked harder. Pulling
  the **Voranmeldungen** series (73311/73421, runs to 2024) would extend the story
  through the energy crisis and strengthen it.
- **Figure 2 candidate:** decompose 2021's +19.8% by sector from `73321-0002` to
  show wholesale trade / mineral-oil / metals driving the amplitude (proves the
  passthrough mechanism). 
- Title/angle (revised): the 8tn turnover number looks more dynamic than GDP, and
  modestly is (~1.4x, gross output amplifies price swings) — but the one
  spectacular data point everyone quotes (+19.8% / "crossed 8tn" in 2021) is half
  an insurance-reclassification mirage. A lesson in reading gross-output tax stats.
  Ties back to the prior essay, which cited 8.1tn at face value.

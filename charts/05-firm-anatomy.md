# Figure 5 — One firm, cut in half at the border

**Purpose:** make the mechanism concrete. A single carmaker's value chain, split by the
national border, with each activity tagged by which statistic sees it. The high-value
work stays home and is visible; assembly moves abroad and is invisible to German GDP.
**Type:** conceptual schematic (boxes + arrows), NOT a data chart.
**Goes:** §"The part outside Germany", the car-company paragraph.

## Content (exact boxes & labels)
A vertical dashed "NATIONAL BORDER" down the middle. Left = HOME, right = ABROAD.

**HOME** (column header: "visible to German GDP · turnover · exports") — 4 boxes,
filled navy/forest, white labels, each tagged `visible`:
- Design & engineering
- IP & patents
- HQ & offices
- Hard components & materials

**ABROAD** (column header: "invisible to German GDP — counted only in Foreign Affiliate
Statistics & host-country GDP") — 2 boxes, ochre-tint fill (`--oi-highlight`) with
`--oi-accent` outline, dark labels, each tagged `invisible`:
- Assembly / volume manufacturing — *the "hands", in a firm-owned plant*
- Finished car — built & sold abroad — *in no German trade data at all*

**Arrows across the border:**
- Thick HOME → ABROAD: "components · IP · engineering" (intra-firm trade, the
  connective tissue). Solid, `--oi-ink-2`.
- Thin ABROAD → HOME: "only the dividend returns — net ~€70bn (2023)". Dashed,
  `--oi-accent`.

## Source & metadata
- Conceptual; the carmaker is illustrative (VW/BMW/Mercedes-style: design at home,
  plants in the US / Mexico / China).
- The €70bn figure: net direct-investment income 2023, Bundesbank balance of payments
  table II.4b (gross outward-FDI income €158.0bn, distributed €99.0bn, debits €87.9bn,
  net €70.1bn). See `../SPINE.md` §G.

## Visual spec
- viewBox ~ `0 0 900 380`. Column headers top. HOME boxes ~300px wide on the left,
  ABROAD boxes ~300px on the right, border line at x≈450 (label "NATIONAL BORDER").
- Home boxes: solid `--oi-brand`/`--oi-brand-2`, **label text in white, 13px, weight
  600 — must be legible** (the failed build rendered black boxes with no visible text).
- Abroad boxes: `--oi-highlight` fill + `--oi-accent` stroke, dark label + light sub.
- `visible` / `invisible` tags small, uppercase, letter-spaced; invisible in ochre.
- Arrows with markers; intra-firm arrow thick, dividend arrow thin/dashed.
- role="img", aria-label describing the home/abroad split.

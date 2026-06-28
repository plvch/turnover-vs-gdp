#!/usr/bin/env python3
"""Fold the FRED quarterly nominal-GDP series (NGDPSAXDCDEQ, seasonally
adjusted, millions of EUR) into annual totals in EUR billion, with YoY growth.

Source: FRED NGDPSAXDCDEQ — Germany, Nominal GDP, Seasonally Adjusted,
Domestic Currency (EUR), Quarterly. Annual = sum of the four SA quarters.
"""
import csv
from collections import defaultdict
from pathlib import Path

SRC = Path(__file__).with_name("gdp_nominal_quarterly_fred_NGDPSAXDCDEQ.csv")

q = defaultdict(dict)  # year -> {quarter_month: value_millions}
with SRC.open() as f:
    for row in csv.DictReader(f):
        d = row["observation_date"]
        year, month = int(d[:4]), int(d[5:7])
        q[year][month] = float(row["NGDPSAXDCDEQ"])

# Only keep complete years (all 4 quarters present)
annual = {}
for year, qs in sorted(q.items()):
    if len(qs) == 4:
        annual[year] = sum(qs.values()) / 1000.0  # millions -> billions

print(f"{'year':>6} {'gdp_eur_bn':>12} {'yoy_%':>8}")
prev = None
out_rows = []
for year, bn in sorted(annual.items()):
    yoy = (bn / prev - 1) * 100 if prev else None
    out_rows.append((year, round(bn, 1), round(yoy, 2) if yoy is not None else ""))
    print(f"{year:>6} {bn:>12.1f} {('%+.2f' % yoy) if yoy is not None else '':>8}")
    prev = bn

# write tidy annual CSV
OUT = Path(__file__).with_name("gdp_nominal_annual.csv")
with OUT.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["year", "gdp_nominal_eur_bn", "yoy_pct"])
    w.writerows(out_rows)
print(f"\nwrote {OUT.name} ({len(out_rows)} years)")

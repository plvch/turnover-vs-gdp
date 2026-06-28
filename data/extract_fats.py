#!/usr/bin/env python3
"""Extract the Germany-controlling slice from the (560MB) Eurostat fats_out2_r2
linear CSV into a small tidy file, and print the turnover progression.

Eurostat outward FATS, NACE Rev.2 vintage covers 2010-2020.
  indic_bp: TUR = turnover (EUR million), EMP = persons employed, ENT = enterprises
  partner : WORLD = all host countries, US, EU27_2020
  nace_r2 : B-S_X_O = business economy total (Industry, construction & services
            excl. public admin); C29_C30 = motor-vehicle manufacturing (the VW slice)
  geo     : DE = Germany as the controlling/compiling country
"""
import csv, sys
from pathlib import Path
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home()/"Downloads/fats_out2_r2_linear_2_0.csv"
OUT = Path(__file__).with_name("fats_de_extract.csv")

KEEP_NACE = {"B-S_X_O", "C", "C29_C30", "G", "K"}
rows = []            # keep ALL partner countries
plabel = {}
with SRC.open(newline="") as fh:
    r = csv.reader(fh); next(r)
    for row in r:
        if len(row) < 16 or row[11] != "DE":
            continue
        nace, indic, part = row[5], row[7], row[9]
        if nace in KEEP_NACE:
            v = row[15].strip()
            rows.append([row[13], indic, nace, part, v if v not in ("", ":") else ""])
            plabel[part] = row[10]

with OUT.open("w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["year", "indic", "nace", "partner", "value_eur_mn"])
    w.writerows(sorted(rows))
print(f"wrote {OUT.name}  ({len(rows)} rows)\n")

# --- helpers ---
def series(indic, nace, part):
    d = {}
    for y, i, n, p, v in rows:
        if i == indic and n == nace and p == part and v:
            d[int(y)] = float(v)        # EUR million (TUR) or persons (EMP)
    return d

YR = 2019  # last pre-COVID full year
wt = series("TUR", "B-S_X_O", "WORLD")          # EUR million
emp_w = series("EMP", "B-S_X_O", "WORLD")        # persons
# host countries = real partners only: drop aggregates (continents, EU, World).
# Keep 2-letter ISO codes plus CN_X_HK (China).
def is_country(p):
    return p == "CN_X_HK" or (len(p) == 2 and p not in {"EU"})
tur_by_part = {p: float(v)/1e6 for y, i, n, p, v in rows
               if i == "TUR" and n == "B-S_X_O" and int(y) == YR and v and is_country(p)}
print(f"\nTop host countries — German-controlled affiliates' turnover, {YR}:")
for p, v in sorted(tur_by_part.items(), key=lambda kv: -kv[1])[:8]:
    print(f"  {p:<7}{plabel.get(p,'')[:24]:<25}{v:>6.3f} tn  {v/(wt[YR]/1e6)*100:>4.0f}% of abroad")

print(f"\nAbroad employment (persons): " +
      "  ".join(f"{y}:{e/1e6:.1f}M" for y, e in sorted(emp_w.items())))
for y in (YR, 2020):
    if wt.get(y) and emp_w.get(y):
        print(f"  turnover/head abroad {y}: {wt[y]*1e6/emp_w[y]:,.0f} EUR "
              f"({wt[y]/1e6:.2f}tn / {emp_w[y]/1e6:.2f}M)")

#!/usr/bin/env python3
"""Voranmeldungen turnover (73311-0001, 2002-2024) vs nominal GDP, break-adjusted.

The 2021 insurance reclassification is a PERMANENT level step (section K jumps
~556bn in 2021 and stays up). We subtract that constant step from 2021 onward:
this cleans the 2021 YoY while preserving 2022-2024 YoY (constant cancels).
Also scans every section x year-pair for any other break.
"""
import csv, statistics as st
from collections import defaultdict
from pathlib import Path
HERE = Path(__file__).parent
def num(s):
    s = s.strip(); return float(s) if s not in ("-", "", ".", "...", "x") else None

# turnover total by year (STR042) + taxpayers (STR040)
tv = defaultdict(dict)
for r in csv.DictReader((HERE/"turnover_73311/73311-0001_en_flat.csv").open(encoding="utf-8-sig"), delimiter=";"):
    tv[int(r["time"])][r["value_variable_code"]] = num(r["value"])

# section-K series + break-scan from 73311-0002
sec = defaultdict(dict); lab = {}
for r in csv.DictReader((HERE/"turnover_73311/0002/73311-0002_en_flat.csv").open(encoding="utf-8-sig"), delimiter=";"):
    if r["value_variable_code"] != "STR042": continue
    seg = r["2_variable_attribute_code"].replace("WZ08-", "")
    if len(seg) == 1 and seg.isalpha():
        v = num(r["value"])
        if v is not None: sec[seg][int(r["time"])] = v/1e6
        lab[seg] = r["2_variable_attribute_label"]
STEP = sec["K"][2021] - sec["K"][2020]   # permanent insurance step, bn

print("break-scan (section base>20bn, |YoY|>40%):")
flags = 0
for c, d in sec.items():
    ys = sorted(d)
    for p, n in zip(ys, ys[1:]):
        if d[p] > 20 and abs(d[n]/d[p]-1) > 0.40:
            print(f"  {n}: sec {c} {lab[c][:28]:<29}{d[p]:.0f}->{d[n]:.0f} ({(d[n]/d[p]-1)*100:+.0f}%)"); flags += 1
print(f"  ({flags} flag; insurance step = {STEP:.0f}bn)\n")

# GDP
gdp = {int(r["year"]): float(r["gdp_nominal_eur_bn"]) for r in csv.DictReader((HERE/"gdp_nominal_annual.csv").open())}

years = sorted(y for y in tv if tv[y].get("STR042") and y in gdp)
rows = []
for y in years:
    t = tv[y]["STR042"]/1e6
    t_adj = t - (STEP if y >= 2021 else 0)
    rows.append(dict(year=y, turn=t, adj=t_adj, gdp=gdp[y], ratio=t_adj/gdp[y],
                     tp=tv[y].get("STR040")))
def yoy(seq): return [None]+[(b/a-1)*100 for a, b in zip(seq, seq[1:])]
for r, ty, ay, gy in zip(rows, yoy([r["turn"] for r in rows]), yoy([r["adj"] for r in rows]), yoy([r["gdp"] for r in rows])):
    r["t_yoy"], r["a_yoy"], r["g_yoy"] = ty, ay, gy
    r["gap"] = (ay-gy) if ay is not None else None

print(f"{'yr':>5}{'turn':>8}{'adj':>8}{'gdp':>8}{'ratio':>7}{'raw_yoy':>9}{'adj_yoy':>9}{'gdp_yoy':>9}{'gap':>8}")
for r in rows:
    fm = lambda v: ("%+.1f" % v) if v is not None else ""
    print(f"{r['year']:>5}{r['turn']:>8.0f}{r['adj']:>8.0f}{r['gdp']:>8.0f}{r['ratio']:>7.3f}"
          f"{fm(r['t_yoy']):>9}{fm(r['a_yoy']):>9}{fm(r['g_yoy']):>9}{fm(r['gap']):>8}")

# amplitude stats on adjusted series, 2005-2024
A = [r["a_yoy"] for r in rows if r["a_yoy"] is not None]
G = [r["g_yoy"] for r in rows if r["g_yoy"] is not None]
def sd(x): return st.pstdev(x)
n=len(A); mA,mG=st.mean(A),st.mean(G)
cov=sum((a-mA)*(b-mG) for a,b in zip(A,G))/n
print(f"\nadj turnover YoY: std {sd(A):.2f}  range {min(A):.1f}..{max(A):.1f} ({max(A)-min(A):.1f}pp)")
print(f"gdp     YoY: std {sd(G):.2f}  range {min(G):.1f}..{max(G):.1f} ({max(G)-min(G):.1f}pp)")
print(f"std ratio {sd(A)/sd(G):.2f}x | beta {cov/sd(G)**2:.2f} | corr {cov/(sd(A)*sd(G)):.2f}  (n={n}, 2005-2024)")
print(f"ratio turnover/gdp (adj): {min(r['ratio'] for r in rows):.2f}-{max(r['ratio'] for r in rows):.2f}")

out = HERE/"voran_turnover_vs_gdp.csv"
with out.open("w", newline="") as f:
    w=csv.writer(f); w.writerow(["year","turnover_raw_bn","turnover_adj_bn","gdp_bn","ratio_adj","raw_yoy","adj_yoy","gdp_yoy","gap_pp","taxpayers"])
    g=lambda v,n=2: round(v,n) if v is not None else ""
    for r in rows:
        w.writerow([r["year"],g(r["turn"],1),g(r["adj"],1),g(r["gdp"],1),g(r["ratio"],3),g(r["t_yoy"],1),g(r["a_yoy"],1),g(r["g_yoy"],1),g(r["gap"],1),int(r["tp"]) if r["tp"] else ""])
print(f"wrote {out.name}")

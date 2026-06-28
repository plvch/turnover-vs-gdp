#!/usr/bin/env python3
"""Merge German taxable turnover (Destatis Umsatzsteuerstatistik, Veranlagungen
73321-0001) with nominal GDP (FRED NGDPSAXDCDEQ), and quantify the relative
amplitude of the two nominal series.

Turnover headline = STR042 "Taxable turnover: supplies and services"
  (= steuerbarer Umsatz aus Lieferungen und Leistungen; 2021 = EUR 8,118.9bn,
   the figure the small-business essay and the Destatis press release cite).
Robustness alt = STR041 "Taxable turnover" (total, incl. intra-Community
  acquisitions and S.13b reverse-charge).
All values converted from EUR 1000 to EUR billion (/1e6).
"""
import csv, statistics as st
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent

def num(s):
    s = s.strip()
    return float(s) if s not in ("-", "", ".", "...", "x") else None

# --- turnover (73321-0001) ---
tv = defaultdict(dict)
src = HERE / "turnover_73321/0001/73321-0001_en_flat.csv"
for r in csv.DictReader(src.open(encoding="utf-8-sig"), delimiter=";"):
    tv[int(r["time"])][r["value_variable_code"]] = num(r["value"])

# --- section K (Financial & insurance) from 73321-0002, to neutralise the
#     2021 break: insurance exempt-turnover coverage change took K from
#     ~88bn to ~801bn (+713bn), all artifact. We revert K to its 2020 level. ---
kK = {}
sec_src = HERE / "turnover_73321/0002/73321-0002_en_flat.csv"
for r in csv.DictReader(sec_src.open(encoding="utf-8-sig"), delimiter=";"):
    if r["value_variable_code"] != "STR042":
        continue
    seg = r["2_variable_attribute_code"].replace("WZ08-", "")
    if seg == "K":
        v = num(r["value"])
        if v is not None:
            kK[int(r["time"])] = v / 1e6
K_BREAK = kK[2021] - kK[2020]  # ~713bn of artificial 2021 increase

# --- nominal GDP (annual, EUR bn) ---
gdp = {}
for r in csv.DictReader((HERE / "gdp_nominal_annual.csv").open()):
    gdp[int(r["year"])] = float(r["gdp_nominal_eur_bn"])

# --- merge on overlapping years ---
years = sorted(y for y in tv if "STR042" in tv[y] and tv[y]["STR042"] is not None and y in gdp)
rows = []
for y in years:
    turn = tv[y]["STR042"] / 1e6            # L&L steuerbarer Umsatz, EUR bn
    turn_adj = turn - (K_BREAK if y == 2021 else 0)   # break-adjusted
    turn_tot = (tv[y].get("STR041") or 0) / 1e6
    g = gdp[y]
    rows.append(dict(year=y, turnover=turn, turnover_adj=turn_adj,
                     turnover_total=turn_tot, gdp=g,
                     ratio=turn / g, ratio_adj=turn_adj / g,
                     taxpayers=tv[y].get("STR040")))

def yoy(seq):
    out = [None]
    for a, b in zip(seq, seq[1:]):
        out.append((b / a - 1) * 100)
    return out

t_yoy = yoy([r["turnover"] for r in rows])
ta_yoy = yoy([r["turnover_adj"] for r in rows])
g_yoy = yoy([r["gdp"] for r in rows])
for r, ty, tay, gy in zip(rows, t_yoy, ta_yoy, g_yoy):
    r["turn_yoy"], r["turn_adj_yoy"], r["gdp_yoy"] = ty, tay, gy
    r["gap"] = (tay - gy) if tay is not None else None   # gap on the CLEAN series

print(f"K-2021 break removed: -{K_BREAK:.0f} bn "
      f"(K {kK[2020]:.0f} -> {kK[2021]:.0f}, reverted to {kK[2020]:.0f})\n")

# --- print table ---
print(f"{'year':>5}{'turn_bn':>9}{'adj_bn':>9}{'gdp_bn':>9}{'ratio':>7}{'r_adj':>7}"
      f"{'t_yoy':>8}{'adj_yoy':>9}{'gdp_yoy':>9}")
for r in rows:
    fm = lambda v: ("%+.2f" % v) if v is not None else ""
    print(f"{r['year']:>5}{r['turnover']:>9.0f}{r['turnover_adj']:>9.0f}{r['gdp']:>9.0f}"
          f"{r['ratio']:>7.3f}{r['ratio_adj']:>7.3f}"
          f"{fm(r['turn_yoy']):>8}{fm(r['turn_adj_yoy']):>9}{fm(r['gdp_yoy']):>9}")

# --- amplitude stats: headline vs break-adjusted, both vs GDP ---
def stats(x):
    return dict(mean=st.mean(x), std=st.pstdev(x), lo=min(x), hi=max(x),
                rng=max(x) - min(x))

def beta_corr(X, Y):  # X on Y
    n = len(X); mx, my = st.mean(X), st.mean(Y)
    cov = sum((a-mx)*(b-my) for a, b in zip(X, Y)) / n
    return cov / st.pstdev(Y)**2, cov / (st.pstdev(X)*st.pstdev(Y))

G = [r["gdp_yoy"] for r in rows if r["gdp_yoy"] is not None]
for label, key in (("HEADLINE (raw)", "turn_yoy"), ("BREAK-ADJUSTED", "turn_adj_yoy")):
    T = [r[key] for r in rows if r[key] is not None]
    ts, gs = stats(T), stats(G)
    b, c = beta_corr(T, G)
    print(f"\n--- {label} turnover YoY vs GDP, 2007-2021 (n={len(T)}) ---")
    print(f"           turnover     gdp")
    for k in ("mean", "std", "lo", "hi", "rng"):
        print(f"{k:>10}{ts[k]:>11.2f}{gs[k]:>8.2f}")
    print(f"std ratio {ts['std']/gs['std']:.2f}x | range ratio {ts['rng']/gs['rng']:.2f}x "
          f"| beta {b:.2f} | corr {c:.2f}")

print(f"\nratio turnover/gdp  raw: {min(r['ratio'] for r in rows):.3f}-"
      f"{max(r['ratio'] for r in rows):.3f}   "
      f"adj: {min(r['ratio_adj'] for r in rows):.3f}-{max(r['ratio_adj'] for r in rows):.3f}")

# --- write merged CSV ---
out = HERE / "turnover_vs_gdp_annual.csv"
with out.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["year", "turnover_LuL_eur_bn", "turnover_LuL_adj_eur_bn",
                "turnover_total_eur_bn", "gdp_nominal_eur_bn",
                "ratio", "ratio_adj", "turnover_yoy_pct", "turnover_adj_yoy_pct",
                "gdp_yoy_pct", "gap_adj_pp", "taxpayers"])
    g = lambda v, n=2: round(v, n) if v is not None else ""
    for r in rows:
        w.writerow([r["year"], g(r["turnover"], 1), g(r["turnover_adj"], 1),
                    g(r["turnover_total"], 1), g(r["gdp"], 1),
                    g(r["ratio"], 4), g(r["ratio_adj"], 4),
                    g(r["turn_yoy"]), g(r["turn_adj_yoy"]), g(r["gdp_yoy"]),
                    g(r["gap"]), int(r["taxpayers"]) if r["taxpayers"] else ""])
print(f"\nwrote {out.name}")

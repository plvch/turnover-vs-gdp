#!/usr/bin/env python3
"""Stitch the two Eurostat outward-FATS vintages into one Germany series 2010-2023
and compare turnover abroad with the home economy.

  fats_out2_r2   (indic_bp:  TUR/EMP/ENT, partner WORLD)     -> 2010-2020
  fats_out_activ (indic_sbs: NETTUR_MEUR/EMP_NR, partner WRL_REST = world) -> 2021-2023
  (WRL_REST = INT_EU27 + EXT_EU27 = world total; verified to match Bundesbank 3.4tn.)
Reads the small 2010-2020 DE extract (data/fats_de_extract.csv) + the 9.4MB 2021+
source; writes a small 2021+ extract and a unified annual CSV.
"""
import csv, sys
from pathlib import Path
from collections import defaultdict
HERE = Path(__file__).parent
SRC21 = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home()/"Downloads/fats_out_activ__custom_21908478_linear_2_0.csv"

# --- 2010-2020 from the saved small extract ---
tur, emp, by_country = {}, {}, defaultdict(dict)   # by_country[year][partner]=turnover_mn
for r in csv.DictReader((HERE/"fats_de_extract.csv").open()):
    if r["nace"] != "B-S_X_O" or not r["value_eur_mn"]:
        continue
    y, p, v = int(r["year"]), r["partner"], float(r["value_eur_mn"])
    if r["indic"] == "TUR":
        if p == "WORLD": tur[y] = v
        by_country[y][p] = v
    elif r["indic"] == "EMP" and p == "WORLD":
        emp[y] = v

# --- 2021-2023 from fats_out_activ (and persist a small extract) ---
small = []
for r in csv.reader(SRC21.open(newline="")):
    if len(r) < 16 or r[11] != "DE" or r[5] not in ("B-S_X_O", "C29_C30"):
        continue
    small.append([r[13], r[7], r[5], r[9], r[15].strip()])
with (HERE/"fats_de_extract_2021.csv").open("w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["year","indic","nace","partner","value"]); w.writerows(sorted(small))
for y, ind, nace, p, v in small:
    if nace != "B-S_X_O" or not v:
        continue
    y = int(y); v = float(v)
    if ind == "NETTUR_MEUR":
        if p == "WRL_REST": tur[y] = v        # world total
        by_country[y][p] = v
    elif ind == "EMP_NR" and p == "WRL_REST":
        emp[y] = v

# --- unified annual series ---
print(f"{'year':>5}{'abroad_tn':>11}{'yoy%':>8}{'US_bn':>8}{'US_sh':>7}{'empl_M':>8}{'per_head_k':>11}")
prev=None
for y in sorted(tur):
    t=tur[y]; us=by_country[y].get("US"); e=emp.get(y)
    yoy=f"{(t/prev-1)*100:+.1f}" if prev else ""
    print(f"{y:>5}{t/1e6:>11.3f}{yoy:>8}{(us or 0)/1e3:>8.0f}{(us/t*100 if us else 0):>6.0f}%"
          f"{(e/1e6 if e else 0):>8.2f}{(t*1e3/e if e else 0):>11.0f}")
    prev=t

# --- top host countries, latest year ---
AGG={"WORLD","WRL_REST","EXT_EU27_2020","INT_EU27_2020","EU27_2020","EU28","OFFSHO","EXT_EU_NAL","EU","AME","ASI","EUR","AFR","OCE"}
LAST=max(tur)
top={p:v for p,v in by_country[LAST].items() if p not in AGG and (p=="CN_X_HK" or len(p)==2)}
print(f"\nTop host countries {LAST} (turnover, EUR bn):")
for p,v in sorted(top.items(),key=lambda kv:-kv[1])[:8]:
    print(f"  {p:<8}{v/1e3:>7.0f} bn  {v/tur[LAST]*100:>4.0f}%")

# --- home comparison ---
HOME_EMPL = {2019: 45.27e6, 2023: 45.92e6}   # Destatis Erwerbstätige (Inland)
vt = {int(r["year"]): float(r["turnover_adj_bn"]) for r in csv.DictReader((HERE/"voran_turnover_vs_gdp.csv").open())}
gp = {int(r["year"]): float(r["gdp_nominal_eur_bn"]) for r in csv.DictReader((HERE/"gdp_nominal_annual.csv").open())}
print("\nabroad vs home, gross turnover per head:")
for y in (2019, 2023):
    ab=tur[y]*1e6/emp[y]; hm=vt[y]*1e9/HOME_EMPL[y]; gdph=gp[y]*1e9/HOME_EMPL[y]
    print(f"  {y}: abroad {ab/1e3:.0f}k/head ({tur[y]/1e6:.2f}tn / {emp[y]/1e6:.1f}M) | "
          f"home turnover {hm/1e3:.0f}k/head ({vt[y]/1e3:.1f}tn / {HOME_EMPL[y]/1e6:.0f}M) | "
          f"home GDP {gdph/1e3:.0f}k/head | ratio {ab/hm:.1f}x")

out=HERE/"fats_abroad_annual.csv"
with out.open("w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["year","turnover_abroad_eur_bn","employees","us_turnover_eur_bn","us_share_pct"])
    for y in sorted(tur):
        us=by_country[y].get("US")
        w.writerow([y,round(tur[y]/1e3,1),int(emp[y]) if emp.get(y) else "",round(us/1e3,1) if us else "",round(us/tur[y]*100,1) if us else ""])
print(f"\nwrote {out.name}")

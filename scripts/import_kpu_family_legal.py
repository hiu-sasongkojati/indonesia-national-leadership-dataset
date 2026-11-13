#!/usr/bin/env python3
"""Add marital status, spouse, number of children and legal status from the KPU candidate filings of 2024.

Input   data/external/raw/candidate_pileg_data_2024.csv   Kuipers' compilation of KPU candidate pages (git ignores it)
Edits   data/persons.csv  (columns marital_status, spouse_name, n_children, legal_status, family_legal_src)

People are matched through the DPR candidacies already in data/candidacies.csv (constituency, party, list
number), so only the 68 people matched in version 0.2 are affected. Values describe the filing of February
2024. Placeholders such as "-" and "No Name" are left empty. The script can be run again safely.
Run from the repository root:  python3 scripts/import_kpu_family_legal.py
"""
import csv, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "data"
KPU = D / "external" / "raw" / "candidate_pileg_data_2024.csv"
csv.field_size_limit(10 ** 9)
NEW = ["marital_status", "spouse_name", "n_children", "legal_status", "family_legal_src"]
MARITAL = {"Sudah": "married", "Belum": "unmarried"}
LEGAL = {"Tidak Memiliki Status Hukum": "none_declared", "Mantan Terpidana": "former_convict",
         "Mantan Terpidana Yang Menjalani Masa Bimbingan": "former_convict_on_parole",
         "Mantan Terpidana Culva": "former_convict_culpa", "Terpidana": "convicted"}
EMPTY = {"", "-", "NA", "NO NAME", "TIDAK ADA", "0", "PASANGAN", "ISTRI", "SUAMI"}


def read(name):
    with open(D / name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


P, O = read("persons.csv"), {o["org_id"]: o for o in read("organizations.csv")}
C = [c for c in read("candidacies.csv") if c["src"] == "kpu2024"]
person = {p["person_id"]: p for p in P}
names = {p["name"].upper(): p["person_id"] for p in P}
dpr = {}
with open(KPU, encoding="utf-8", errors="replace", newline="") as f:
    for k in csv.DictReader(f):
        if k["level"] == "DPR":
            dpr.setdefault((k["dapil"].strip(), k["party_list_number"]), []).append(k)

for p in P:
    for c in NEW:
        p[c] = ""
filled, spouses_in_dataset = 0, []
for c in C:
    long = O[c["party_org_id"]]["name_long"].split(" (")[0].lower()
    hits = [k for k in dpr.get((c["constituency"], c["list_number"]), []) if k["party_name"].strip().lower() == long]
    if len(hits) != 1:
        sys.exit(f"{person[c['person_id']]['name']}: {len(hits)} KPU rows")
    k, p = hits[0], person[c["person_id"]]
    p["marital_status"] = MARITAL.get(k["marital_status"].strip(), "")
    sp = " ".join(k["spouse_name"].split())
    p["spouse_name"] = "" if sp.upper() in EMPTY else sp
    n = k["number_kids"].strip()
    p["n_children"] = n if n.isdigit() and (n != "0" or p["marital_status"]) else ""
    p["legal_status"] = LEGAL.get(k["corruption_status"].strip(), "")
    if any(p[x] for x in NEW[:4]):
        p["family_legal_src"] = "kpu2024"
        filled += 1
    if p["spouse_name"] and p["spouse_name"].upper() in names:
        spouses_in_dataset.append((p["name"], p["spouse_name"]))

cols = list(P[0].keys())
for c in NEW:
    cols.remove(c)
at = cols.index("highest_degree_src") + 1
cols[at:at] = NEW
with open(D / "persons.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, quoting=csv.QUOTE_ALL, lineterminator="\n")
    w.writeheader()
    w.writerows(P)
print(f"filled for {filled} people; marital {sum(bool(p['marital_status']) for p in P)}, spouse named "
      f"{sum(bool(p['spouse_name']) for p in P)}, children {sum(bool(p['n_children']) for p in P)}, legal status "
      f"{sum(bool(p['legal_status']) for p in P)}; spouses who are in the dataset: {spouses_in_dataset or 'none'}")

#!/usr/bin/env python3
"""Fill the outcome and vote count of the 68 DPR candidacies of 2024.

Source S029: the list of 580 candidates declared elected by the KPU, as published on a KPU website. A
candidate on the list is coded `won` with the vote count shown; a candidate absent from it is coded `lost`.
The list records who was declared elected, not who was sworn in or who still holds the seat.
Run once from the repository root:  python3 scripts/add_dpr_results_2024.py
"""
import csv, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1] / "data"
WON = {"Ace Hasan Syadzily": 107704, "Ahmad Basarah": 89769, "Ahmad Doli Kurnia": 141846, "Ahmad Heryawan": 145034,
       "Ahmad Muzani": 110161, "Ahmad Sahroni": 163292, "Ahmad Syaikhu": 165976, "Al Muzzammil Yusuf": 65452,
       "Bambang Soesatyo": 80468, "Bambang Wuryanto": 118384, "Benny K. Harman": 79335, "Budisatrio Djiwandono": 131569,
       "Deddy Sitorus": 59335, "Dede Yusuf": 210179, "Dedi Mulyadi": 375658, "Eddy Soeparno": 66703,
       "Edhie Baskoro Yudhoyono": 318223, "Eko Hendro Purnomo": 93673, "Erwin Aksa": 186897, "Fadli Zon": 149258,
       "Faisol Riza": 214779, "Habiburokhman": 96914, "Hanif Dhakiri": 88244, "Herman Khaeron": 78033,
       "Hidayat Nur Wahid": 227974, "Hinca Pandjaitan": 74375, "Ida Fauziyah": 76092, "Irfan Yusuf": 77433,
       "Jazilul Fawaid": 80974, "Jazuli Juwaini": 82685, "Kahar Muzakir": 185597, "Komarudin Watubun": 278024,
       "Lestari Moerdijat": 107293, "M. Sarmuji": 183045, "Maman Abdurrahman": 203514, "Meutya Hafid": 147004,
       "Muhammad Kholid": 107251, "Mukhtarudin": 92192, "Nusron Wahid": 204248, "Prasetyo Hadi": 105580,
       "Puan Maharani": 297366, "Rachmat Gobel": 195322, "Rahayu Saraswati": 52932, "Rusdi Kirana": 121080,
       "Saan Mustopa": 74695, "Said Abdullah": 528815, "Saleh Daulay": 77914, "Sari Yuliati": 119444,
       "Sohibul Iman": 76661, "Sufmi Dasco Ahmad": 119692, "Sugiono": 62855, "Teuku Riefky Harsya": 88005,
       "Willy Aditya": 142639, "Yasonna Laoly": 83045}
NO_SEATS = {"party_psi", "party_pbb", "party_garuda"}       # parties that won no DPR seat in 2024


def read(n):
    with open(D / n, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


C, S = read("candidacies.csv"), read("sources.csv")
name = {p["person_id"]: p["name"] for p in read("persons.csv")}
if not any(s["source_id"] == "S029" for s in S):
    S.append({"source_id": "S029", "type": "official", "title": "580 Daftar Nama Caleg DPR RI 2024 yang Lolos ke Senayan",
              "publisher": "KPU Provinsi Papua Pegunungan",
              "url": "https://papuapegunungan.kpu.go.id/blog/read/1788_580-daftar-nama-caleg-dpr-ri-2024-yang-lolos-ke-senayan",
              "date_published": "2025-11-03", "date_retrieved": "2026-11-13",
              "note": "Candidates declared elected to the DPR by the KPU, by constituency, with vote counts"})
seen = set()
for c in C:
    c.setdefault("votes", "")
    c.setdefault("outcome_source_id", "")
    if c["election_type"] != "legislative":
        continue
    n = name[c["person_id"]]
    seen.add(n)
    c["outcome_source_id"] = "S029"
    if n in WON:
        c["outcome"], c["votes"] = "won", str(WON[n])
    else:
        c["outcome"] = "lost"
        extra = "the party won no DPR seat" if c["party_org_id"] in NO_SEATS else "not on the KPU list of elected candidates"
        c["note"] = "; ".join(x for x in (c["note"], extra) if x and extra not in c["note"])
if set(WON) - seen:
    sys.exit(f"names not matched: {set(WON) - seen}")
cols = list(C[0].keys())
for col, after in (("votes", "vote_share_pct"), ("outcome_source_id", "outcome")):
    cols.remove(col)
    cols.insert(cols.index(after) + 1, col)
for n, rows in (("candidacies.csv", C), ("sources.csv", S)):
    with open(D / n, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols if n == "candidacies.csv" else list(rows[0].keys()),
                           quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
leg = [c for c in C if c["election_type"] == "legislative"]
print("won", sum(c["outcome"] == "won" for c in leg), "lost", sum(c["outcome"] == "lost" for c in leg))
print("lost:", ", ".join(name[c["person_id"]] for c in leg if c["outcome"] == "lost"))

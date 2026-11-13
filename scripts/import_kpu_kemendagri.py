#!/usr/bin/env python3
"""Version 0.2: add the KPU legislative candidate profiles of 2024 and the Kemendagri party register.

Inputs   data/external/raw/candidate_pileg_data_2024.csv            Kuipers' scrape of the KPU candidate pages, Feb 2024
                                                       (not committed: 128 MB and not ours to redistribute)
         data/external/kemendagri/pengurus_partai_politik_2026-11-12.csv
Edits    data/persons.csv, memberships.csv, candidacies.csv, organizations.csv, sources.csv

Run once from the repository root:  python3 scripts/import_kpu_kemendagri.py
It stops if source S006 is already present, so it cannot be applied twice.

KPU fields not imported here: address, motivation and platform. Marital status, spouse, children and
legal status are added by scripts/import_kpu_family_legal.py. The KPU "birth_place" column holds the candidate's district of residence,
not the place of birth, and the "education" column is not the highest degree, so neither is used.
"""
import csv, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "data"
KPU = D / "external" / "raw" / "candidate_pileg_data_2024.csv"
KEM = D / "external" / "kemendagri" / "pengurus_partai_politik_2026-11-12.csv"
csv.field_size_limit(10 ** 9)


def read(name):
    with open(D / name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write(name, rows, cols):
    with open(D / name, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader()
        w.writerows({c: r.get(c, "") for c in cols} for r in rows)
    print(f"{name:20s} {len(rows):4d} rows")


P, M, C, O, S = (read(n) for n in ("persons.csv", "memberships.csv", "candidacies.csv",
                                   "organizations.csv", "sources.csv"))
if any(s["source_id"] == "S006" for s in S):
    sys.exit("already applied: S006 is in sources.csv")
pid = {p["name"]: p["person_id"] for p in P}
person = {p["person_id"]: p for p in P}

# ------------------------------------------------------------------ sources
US = re.compile(r"^(\d{1,2})/(\d{1,2})/(\d{2})$")          # dates a spreadsheet app rewrote as M/D/YY
for s in S:
    for c in ("date_published", "date_retrieved"):
        m = US.match(s[c])
        if m:
            s[c] = f"20{m[3]}-{int(m[1]):02d}-{int(m[2]):02d}"
S += [
    {"source_id": "S005", "type": "register", "title": "Data pengurus partai politik (dataset 888)",
     "publisher": "Kementerian Dalam Negeri, Pelita",
     "url": "https://pelita.kemendagri.go.id/kemendagri/dataset/888/tabel-data", "date_published": "",
     "date_retrieved": "2026-11-12",
     "note": "Chair and secretary general of 24 parties. Downloaded 12 Nov 2026, but the entries match boards "
             "in place before mid 2023 (Giring Ganesha chairs PSI, Johnny G. Plate is NasDem secretary general). "
             "Confirms that a post was held, not that it is held now. Raw file in data/external/kemendagri/"},
    {"source_id": "S006", "type": "register", "title": "Indonesian Legislative Candidate Profiles, 2024",
     "publisher": "Nicholas Kuipers, scraped from KPU candidate pages", "url": "https://nicholaskuipers.com/data",
     "date_published": "2024-02", "date_retrieved": "2026-11-12",
     "note": "About 256,000 DPR, DPRD I and DPRD II candidates. Fields are the candidate's own filing; many "
             "candidates closed their profile, leaving only name, party, constituency and gender"},
]

# ------------------------------------------------- organizations: one Garuda
for o in O:
    if o["org_id"] == "party_garuda":
        o["name_long"] = "Partai Garda Republik Indonesia (Partai Garuda)"
        o["note"] = ("Name on the KPU ballot of 2024; Kemendagri lists it as Partai Garda Perubahan Indonesia and "
                     "Wikidata as Partai Gerakan Perubahan Indonesia")
O = [o for o in O if o["org_id"] != "party_garda"]
dup = [m for m in M if m["org_id"] == "party_garda"]
for m in dup:
    if any(x["person_id"] == m["person_id"] and x["org_id"] == "party_garuda" for x in M):
        M.remove(m)                                       # Yohanna Murtika had the same party twice
    else:
        m["org_id"] = "party_garuda"

# ---------------------------------------------------------- KPU candidates
ACCEPT = {  # name in persons.csv: (fragment of the KPU ballot name, constituency, confidence, note)
 "Ace Hasan Syadzily": ("ACE HASAN SYADZILY", "JAWA BARAT II", "high", ""),
 "Afriansyah Noor": ("AFRIANSYAH NOOR", "JAWA BARAT V", "high", ""),
 "Ahmad Ali": ("AHMAD H. M. ALI", "DKI JAKARTA I", "high", ""),
 "Ahmad Basarah": ("AHMAD BASARAH", "JAWA TIMUR V", "high", ""),
 "Ahmad Doli Kurnia": ("AHMAD DOLI KURNIA TANDJUNG", "SUMATERA UTARA III", "high", ""),
 "Ahmad Heryawan": ("AHMAD HERYAWAN", "JAWA BARAT II", "high", ""),
 "Ahmad Muzani": ("AHMAD MUZANI", "LAMPUNG I", "high", ""),
 "Ahmad Sahroni": ("AHMAD SAHRONI", "DKI JAKARTA III", "high", ""),
 "Ahmad Syaikhu": ("AHMAD SYAIKHU", "JAWA BARAT VII", "high", ""),
 "Al Muzzammil Yusuf": ("AL MUZZAMMIL YUSUF", "LAMPUNG I", "high", ""),
 "Bambang Soesatyo": ("BAMBANG SOESATYO", "JAWA TENGAH VII", "high", ""),
 "Bambang Wuryanto": ("BAMBANG WURYANTO", "JAWA TENGAH IV", "high", ""),
 "Benny K. Harman": ("BENNY KABUR HARMAN", "NUSA TENGGARA TIMUR I", "high", ""),
 "Budisatrio Djiwandono": ("BUDISATRIO DJIWANDONO", "KALIMANTAN TIMUR", "high", ""),
 "Deddy Sitorus": ("DEDDY YEVRI HANTERU SITORUS", "KALIMANTAN UTARA", "high", ""),
 "Dede Yusuf": ("DEDE YUSUF MACAN EFFENDI", "JAWA BARAT II", "high", ""),
 "Dedi Mulyadi": ("DEDI MULYADI", "JAWA BARAT VII", "high", ""),
 "Djarot Saiful Hidayat": ("DJAROT SAIFUL HIDAYAT", "SUMATERA UTARA III", "high", ""),
 "Eddy Soeparno": ("EDDY SOEPARNO", "JAWA BARAT III", "high", ""),
 "Edhie Baskoro Yudhoyono": ("EDHIE BASKORO YUDHOYONO", "JAWA TIMUR VII", "high", ""),
 "Eko Hendro Purnomo": ("EKO HENDRO PURNOMO", "DKI JAKARTA I", "high", ""),
 "Erwin Aksa": ("ERWIN AKSA", "DKI JAKARTA III", "high", ""),
 "Fadli Zon": ("FADLI ZON", "JAWA BARAT V", "high", ""),
 "Faisol Riza": ("FAISOL RIZA", "JAWA TIMUR II", "high", ""),
 "Grace Natalie": ("GRACE NATALIE LOUISA", "DKI JAKARTA III", "high", ""),
 "Habiburokhman": ("HABIBUROKHMAN", "DKI JAKARTA I", "high", ""),
 "Hanif Dhakiri": ("HANIF DHAKIRI", "JAWA TENGAH X", "high", ""),
 "Herman Khaeron": ("HERMAN KHAERON", "JAWA BARAT VIII", "high", ""),
 "Hidayat Nur Wahid": ("HIDAYAT NUR WAHID", "DKI JAKARTA II", "high", ""),
 "Hinca Pandjaitan": ("HINCA I.P. PANDJAITAN", "SUMATERA UTARA III", "high", ""),
 "Ida Fauziyah": ("IDA FAUZIYAH", "DKI JAKARTA II", "high", ""),
 "Irfan Yusuf": ("MOCHAMAD IRFAN YUSUF", "JAWA TIMUR VIII", "high", ""),
 "Jazilul Fawaid": ("JAZILUL FAWAID", "JAWA TIMUR X", "high", ""),
 "Jazuli Juwaini": ("JAZULI JUWAINI", "BANTEN II", "high", ""),
 "Kahar Muzakir": ("KAHAR MUZAKIR", "SUMATERA SELATAN I", "high", ""),
 "Komarudin Watubun": ("KAMARUDIN WATUBUN", "PAPUA TENGAH", "high", "KPU spells the name Kamarudin; birth date matches Wikidata"),
 "Lestari Moerdijat": ("LESTARI MOERDIJAT", "JAWA TENGAH II", "high", ""),
 "Lodewijk F. Paulus": ("LODEWIJK F. PAULUS", "LAMPUNG I", "high", ""),
 "M. Sarmuji": ("M. SARMUJI", "JAWA TIMUR VI", "high", ""),
 "Maman Abdurrahman": ("MAMAN ABDURRAHMAN", "KALIMANTAN BARAT I", "high", ""),
 "Meutya Hafid": ("MEUTYA HAFID", "SUMATERA UTARA I", "high", ""),
 "Muhammad Kholid": ("MUHAMMAD KHOLID", "JAWA BARAT VI", "medium", "only DPR candidate of that name; PKS"),
 "Mukhtarudin": ("MUKHTARUDIN", "KALIMANTAN TENGAH", "high", ""),
 "Nusron Wahid": ("NUSRON WAHID", "JAWA TENGAH II", "high", ""),
 "Panel Barus": ("PANEL BARUS", "RIAU I", "high", ""),
 "Prasetyo Hadi": ("PRASETYO HADI", "JAWA TENGAH VI", "high", ""),
 "Puan Maharani": ("PUAN MAHARANI", "JAWA TENGAH V", "high", ""),
 "Rachmat Gobel": ("RACHMAT GOBEL", "GORONTALO", "high", ""),
 "Rahayu Saraswati": ("RAHAYU SARASWATI", "DKI JAKARTA III", "high", ""),
 "Raja Juli Antoni": ("RAJA JULI ANTONI", "RIAU I", "high", ""),
 "Rusdi Kirana": ("RUSDI KIRANA", "JAWA TIMUR VIII", "high", ""),
 "Saan Mustopa": ("SAAN MUSTOPA", "JAWA BARAT VII", "high", ""),
 "Said Abdullah": ("SAID ABDULLAH", "JAWA TIMUR XI", "high", ""),
 "Saleh Daulay": ("SALEH PARTAONAN DAULAY", "SUMATERA UTARA II", "high", ""),
 "Sari Yuliati": ("SARI YULIATI", "NUSA TENGGARA BARAT II", "high", ""),
 "Satrio Dimas Adityo": ("SATRIO DIMAS ADITYO", "JAWA BARAT IV", "high", ""),
 "Sohibul Iman": ("SOHIBUL IMAN", "JAWA BARAT XI", "high", ""),
 "Sufmi Dasco Ahmad": ("SUFMI DASCO AHMAD", "BANTEN III", "high", ""),
 "Sugiono": ("SUGIONO", "JAWA TENGAH I", "high", "Gerindra candidate; profile closed"),
 "Supratman Andi Agtas": ("SUPRATMAN, S.H.", "NUSA TENGGARA BARAT I", "medium", "ballot name Dr. Supratman, Gerindra; birth date matches Wikidata"),
 "Teuku Riefky Harsya": ("TEUKU RIEFKY HARSYA", "ACEH I", "high", ""),
 "Viktor Laiskodat": ("VIKTOR BUNGTILU LAISKODAT", "NUSA TENGGARA TIMUR II", "high", ""),
 "Viva Yoga Mauladi": ("VIVA YOGA MAULADI", "JAWA TIMUR X", "high", ""),
 "Willy Aditya": ("WILLY ADITYA", "JAWA TIMUR XI", "high", ""),
 "Yandri Susanto": ("YANDRI SUSANTO", "BANTEN II", "high", ""),
 "Yasonna Laoly": ("YASONNA H. LAOLY", "SUMATERA UTARA I", "high", ""),
 "Yohanna Murtika": ("YOHANNA MURTIKA", "SUMATERA SELATAN II", "high", ""),
 "Yovianes Mahar": ("YOVIANES MAHAR", "JAWA BARAT X", "high", ""),
}
PARTY = {"Partai Kebangkitan Bangsa": "party_pkb", "Partai Gerakan Indonesia Raya": "party_gerindra",
         "Partai Demokrasi Indonesia Perjuangan": "party_pdip", "Partai Golongan Karya": "party_golkar",
         "Partai NasDem": "party_nasdem", "Partai Keadilan Sejahtera": "party_pks",
         "Partai Amanat Nasional": "party_pan", "Partai Demokrat": "party_demokrat",
         "Partai Solidaritas Indonesia": "party_psi", "Partai Bulan Bintang": "party_pbb",
         "Partai Garda Republik Indonesia": "party_garuda"}
RELIGION = {"Islam": "Islam", "Kristen Protestan": "Protestant", "Kristen Katholik": "Catholic",
            "Hindu": "Hindu", "Budha": "Buddhist", "Konghucu": "Confucian"}


def degree_from_titles(ballot):
    """Lowest degree the ballot titles prove; empty when the ballot shows none."""
    t = ballot.replace(" ", "")
    if re.search(r"(^|[.,])Dr\.(?!\(H\.?C)", t) or "Ph.D" in t or re.search(r"Dr\.Ing", t):
        return "S3"
    if re.search(r",M\.|,MA\.?|,M\.?B\.?A|,LL\.M|,M\.Sc|,M\.Si|,M\.Kn|,M\.Hum|,M\.Ag|,M\.T|,M\.Ed|,M\.IP", t):
        return "S2"
    if re.search(r",S\.[A-Za-z]|,SE\b|,SH\b|,B\.Com|,B\.Sc|,Lc\b|(^|\.)Ir\.|(^|\.)Dr[sa]\.", t):
        return "S1"
    if re.search(r",A\.Md", t):
        return "diploma"
    return ""


rows = []
with open(KPU, encoding="utf-8", errors="replace", newline="") as f:
    for k in csv.DictReader(f):
        if k["level"] == "DPR":
            rows.append(k)
conflicts, n_rel, n_deg, n_bd = [], 0, 0, 0
for name, (frag, dapil, conf, note) in ACCEPT.items():
    hit = [k for k in rows if frag in k["name"].upper() and k["dapil"].strip() == dapil]
    if len(hit) != 1:
        sys.exit(f"{name}: {len(hit)} KPU rows match")
    k, i = hit[0], pid[name]
    p = person[i]
    srcs = set(filter(None, p["bio_src"].split(";")))
    is_open = k["birth_date"] not in ("", "NA")
    g = {"LAKI - LAKI": "M", "PEREMPUAN": "F"}.get(k["gender"].strip(), "")
    if g and not p["gender"]:
        p["gender"] = g; srcs.add("kpu2024")
    elif g and g != p["gender"]:
        conflicts.append(f"{name}: gender {p['gender']} (Wikidata) vs {g} (KPU)")
    if is_open:
        d, mth, y = k["birth_date"].split("-")
        bd = f"{y}-{mth}-{d}"
        if p["birth_date"] and p["birth_date"] != bd and not bd.startswith(p["birth_date"]):
            conflicts.append(f"{name}: birth date {p['birth_date']} (Wikidata) vs {bd} (KPU); KPU kept")
        if p["birth_date"] != bd:
            p["birth_date"] = bd; n_bd += 1
        srcs.add("kpu2024")
        rel = RELIGION.get(k["religion"].strip(), "")
        if rel:
            p["religion"] = rel; n_rel += 1
    deg = degree_from_titles(k["name"])
    if deg:
        p["highest_degree"], p["highest_degree_src"] = deg, "kpu2024 ballot titles, lower bound"; n_deg += 1
    p["bio_src"] = ";".join(sorted(srcs))
    party = PARTY[k["party_name"].strip()]
    C.append({"candidacy_id": f"C{len(C) + 1:03d}", "person_id": i, "election_type": "legislative",
              "election_year": "2024", "round": "", "position": "DPR", "running_mate": "", "vote_share_pct": "",
              "outcome": "", "src": "kpu2024", "source_id": "S006", "confidence": conf,
              "constituency": dapil, "party_org_id": party, "list_number": k["party_list_number"],
              "declared_occupation": "" if k["occupation"] in ("", "NA") else k["occupation"].strip(),
              "profile_open": "1" if is_open else "0", "note": note})
    # the party that nominated the person is documentary evidence of membership in 2023 and 2024
    linked = [m for m in M if m["person_id"] == i and (m["org_id"] == party or
              next((o["parent_org_id"] for o in O if o["org_id"] == m["org_id"]), "") == party)]
    for m in linked:
        if m["src"] == "wikidata":
            m.update(src="kpu2024", source_id="S006", confidence="high",
                     note="nominated by this party for the DPR in 2024; Wikidata P102 agrees")
    if not linked:
        M.append({"membership_id": "", "person_id": i, "org_id": party, "role": "member", "role_level": "member",
                  "basis": "party_affiliation", "start_date": "", "end_date": "", "status_asof": "unknown",
                  "snapshot_layer": "", "in_snapshot": "0", "src": "kpu2024", "source_id": "S006",
                  "confidence": "high", "note": "nominated by this party for the DPR in 2024"})

# ------------------------------------------------------- Kemendagri register
kem = {r["NAMA PARTAI"].strip(): r for r in csv.DictReader(open(KEM, encoding="utf-8", newline=""))}
KEM_NOTE = "post listed in the Kemendagri register (entries from before mid 2023)"
CONFIRM = [  # existing rows whose post the register confirms
    ("Muhaimin Iskandar", "party_pkb_dpp"), ("Hasanuddin Wahid", "party_pkb_dpp"),
    ("Prabowo Subianto", "party_gerindra_dpp"), ("Megawati Soekarnoputri", "party_pdip_dpp"),
    ("Hasto Kristiyanto", "party_pdip_dpp"), ("Surya Paloh", "party_nasdem_dpp"),
    ("Agus Harimurti Yudhoyono", "party_demokrat_dpp"), ("Zulkifli Hasan", "party_pan_dpp"),
    ("Airlangga Hartarto", "party_golkar"), ("Lodewijk F. Paulus", "party_golkar"),
    ("Said Iqbal", "party_buruh"), ("Anis Matta", "party_gelora"), ("Ahmad Ridha Sabana", "party_garuda"),
]
for name, org in CONFIRM:
    hits = [m for m in M if m["person_id"] == pid[name] and m["org_id"] == org and m["role"] not in ("", "member")]
    if len(hits) != 1:
        sys.exit(f"confirm {name} {org}: {len(hits)} rows")
    m = hits[0]
    if m["in_snapshot"] == "1":
        m["role_src"], m["role_source_id"] = "kemendagri", "S005"
    else:
        m["src"], m["source_id"] = "kemendagri", "S005"
    m["note"] = "; ".join(x for x in (m["note"], KEM_NOTE + "; dates from background knowledge") if x)
NEW = [  # posts the register lists that the dataset did not hold; end dates from background knowledge
    ("Ahmad Muzani", "party_gerindra_dpp", "Sekretaris Jenderal", "", "2025", "past", "succeeded by Sugiono in 2025"),
    ("Ahmad Syaikhu", "party_pks_dpp", "Presiden PKS", "2020", "2025", "past", "succeeded by Al Muzzammil Yusuf in 2025"),
    ("Teuku Riefky Harsya", "party_demokrat_dpp", "Sekretaris Jenderal", "2020", "2025", "past", "succeeded by Herman Khaeron in 2025"),
    ("Eddy Soeparno", "party_pan_dpp", "Sekretaris Jenderal", "", "2024", "past", "succeeded by Eko Hendro Purnomo in 2024"),
    ("Yusril Ihza Mahendra", "party_pbb", "Ketua Umum", "", "2024", "past", "stepped down in 2024"),
    ("Afriansyah Noor", "party_pbb", "Sekretaris Jenderal", "", "", "unknown", ""),
    ("Yohanna Murtika", "party_garuda", "Sekretaris Jenderal", "", "", "unknown", ""),
]
for name, org, role, s, e, st, note in NEW:
    lvl = "head" if role in ("Ketua Umum", "Presiden PKS") else "executive_board"
    M.append({"membership_id": "", "person_id": pid[name], "org_id": org, "role": role, "role_level": lvl,
              "basis": "elected" if lvl == "head" else "appointed", "start_date": s, "end_date": e,
              "status_asof": st, "snapshot_layer": "", "in_snapshot": "0", "src": "kemendagri",
              "source_id": "S005", "confidence": "high" if st == "past" else "medium",
              "note": "; ".join(x for x in (KEM_NOTE, ("end date from background knowledge: " + note) if note else "") if x)})
for m in M:
    if not m["membership_id"]:
        m["membership_id"] = f"M{max(int(x['membership_id'][1:]) for x in M if x['membership_id']) + 1:04d}"

# ---------------------------------------------------------------- write back
pcols = list(P[0].keys())
if "highest_degree_src" not in pcols:
    pcols.insert(pcols.index("highest_degree") + 1, "highest_degree_src")
write("persons.csv", P, pcols)
write("memberships.csv", M, list(read("memberships.csv")[0].keys()))
write("candidacies.csv", C, ["candidacy_id", "person_id", "election_type", "election_year", "round", "position",
                             "running_mate", "vote_share_pct", "outcome", "constituency", "party_org_id",
                             "list_number", "declared_occupation", "profile_open", "src", "source_id",
                             "confidence", "note"])
write("organizations.csv", O, list(O[0].keys()))
write("sources.csv", S, list(S[0].keys()))
print(f"KPU matches {len(ACCEPT)}; birth dates set {n_bd}; religion {n_rel}; degree from titles {n_deg}")
print("conflicts:"); [print("  " + c) for c in conflicts]
print("Kemendagri parties not in the dataset:", "; ".join(
    f"{k} ({v['NAMA KETUA UMUM'].strip()} / {v['NAMA SEKERTARIS JENDERAL (SEKJEN)'].strip()})" for k, v in kem.items()
    if k not in ("Partai Kebangkitan Bangsa", "Partai Gerakan Indonesia Raya", "Partai Demokrasi Indonesia Perjuangan",
                 "Partai Golongan Karya", "Partai Keadilan Sejahtera", "Partai Amanat Nasional", "Partai Demokrat",
                 "Partai Bulan Bintang", "Partai Garda Perubahan Indonesia", "Partai Buruh",
                 "Partai Gelombang Rakyat Indonesia", "Partai Nasional Demokrat", "Partai Solidaritas Indonesia")))

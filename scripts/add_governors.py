#!/usr/bin/env python3
"""Version 0.2: code the governors of all 38 provinces as of 13 November 2026.

Executive leadership below the national level is limited to the provinces: governors, and acting
governors where the elected governor is suspended. Vice governors, regents and mayors are out of scope.

Sources  S009 Wikipedia list of sitting governors; S010 Jakarta Post on the suspended Riau governor;
         S011 Wikipedia biographies (kinship and security background); S003 Wikidata for gender,
         birth date, birthplace and party statements (low confidence).
Edits    data/persons.csv, organizations.csv, memberships.csv, ties.csv, education.csv, sources.csv
Run once from the repository root:  python3 scripts/add_governors.py   (stops if S009 exists)
"""
import csv, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1] / "data"


def read(n):
    with open(D / n, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write(n, rows, cols=None):
    cols = cols or list(rows[0].keys())
    with open(D / n, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader()
        w.writerows({c: r.get(c, "") for c in cols} for r in rows)
    print(f"{n:18s} {len(rows):4d} rows")


P, O, M, T, E, S = (read(n) for n in ("persons.csv", "organizations.csv", "memberships.csv", "ties.csv",
                                      "education.csv", "sources.csv"))
if any(s["source_id"] == "S009" for s in S):
    sys.exit("already applied")
S += [
    {"source_id": "S009", "type": "encyclopedia", "title": "Daftar gubernur dan wakil gubernur di Indonesia",
     "publisher": "Wikipedia bahasa Indonesia", "url": "https://id.wikipedia.org/wiki/Daftar_gubernur_dan_wakil_gubernur_di_Indonesia",
     "date_published": "", "date_retrieved": "2026-11-13", "note": "Sitting governors of 38 provinces with the start of the current term"},
    {"source_id": "S010", "type": "news", "title": "Court doubles suspended Riau governor's sentence to four years",
     "publisher": "The Jakarta Post", "url": "https://www.thejakartapost.com/indonesia/2026/10/07/court-doubles-suspended-riau-governors-sentence-to-four-years",
     "date_published": "2026-10-07", "date_retrieved": "2026-11-13", "note": "Abdul Wahid remains suspended governor of Riau"},
    {"source_id": "S011", "type": "encyclopedia", "title": "Biographies of Bobby Nasution, Andi Sudirman Sulaiman, Ahmad Luthfi, Mathius D. Fakhiri, Zainal Arifin Paliwang, Andi Sumangerukka and Yulius Selvanus",
     "publisher": "Wikipedia bahasa Indonesia", "url": "https://id.wikipedia.org/", "date_published": "", "date_retrieved": "2026-11-13",
     "note": "Kinship, police and army careers, academy classes"},
]

# province org_id, province name, governor, Wikidata QID, gender, birth date, birthplace, start of term, parties (Wikidata P102)
GOV = [
 ("reg_aceh", "Aceh", "Muzakir Manaf", "Q17410816", "M", "1964-04-03", "Seunuddon", "2025-02-12", ["party_aceh"]),
 ("reg_sumut", "Sumatera Utara", "Bobby Nasution", "Q54200649", "M", "1991-07-05", "Medan", "2025-02-20", ["party_pdip:2020:2024", "party_gerindra:2024:"]),
 ("reg_sumbar", "Sumatera Barat", "Mahyeldi Ansharullah", "Q17410383", "M", "1966-12-25", "Bukittinggi", "2025-02-20", ["party_pks"]),
 ("reg_riau", "Riau", "SF Hariyanto", "Q124792512", "M", "1965-04-30", "Pekanbaru", "2025-11-05", []),
 ("reg_jambi", "Jambi", "Al Haris", "Q25466192", "M", "1973-11-23", "Sekancing", "2025-02-20", []),
 ("reg_sumsel", "Sumatera Selatan", "Herman Deru", "Q16180910", "M", "1967-11-17", "Belitang", "2025-02-20", ["party_nasdem"]),
 ("reg_bengkulu", "Bengkulu", "Helmi Hasan", "Q25466119", "M", "1979-11-29", "Lampung", "2025-02-20", ["party_pan"]),
 ("reg_lampung", "Lampung", "Rahmat Mirzani Djausal", "Q123874198", "M", "1980-03-18", "Kotabumi", "2025-02-20", ["party_gerindra"]),
 ("reg_babel", "Kepulauan Bangka Belitung", "Hidayat Arsani", "Q16181271", "M", "1963-08-21", "Pangkal Pinang", "2025-04-17", ["party_golkar"]),
 ("reg_kepri", "Kepulauan Riau", "Ansar Ahmad", "Q49250480", "M", "1964-04-10", "Kijang Kota", "2025-02-20", ["party_golkar"]),
 ("reg_jateng", "Jawa Tengah", "Ahmad Luthfi", "Q85988523", "M", "1966-11-22", "Surabaya", "2025-02-20", []),
 ("reg_banten", "Banten", "Andra Soni", "Q109439643", "M", "1976-08-12", "Payakumbuh", "2025-02-20", ["party_gerindra"]),
 ("reg_bali", "Bali", "I Wayan Koster", "Q54805204", "M", "1962-10-20", "Singaraja", "2025-02-20", ["party_pdip"]),
 ("reg_ntb", "Nusa Tenggara Barat", "Lalu Muhamad Iqbal", "Q65208371", "M", "1972-06-10", "Praya", "2025-02-20", []),
 ("reg_ntt", "Nusa Tenggara Timur", "Emanuel Melkiades Laka Lena", "Q96988693", "M", "1976-12-10", "Kupang", "2025-02-20", ["party_golkar"]),
 ("reg_kalbar", "Kalimantan Barat", "Ria Norsan", "Q25469767", "M", "1967-12-17", "Mempawah Hilir", "2025-02-20", ["party_golkar"]),
 ("reg_kalteng", "Kalimantan Tengah", "Agustiar Sabran", "Q28723899", "M", "1972-08-17", "Sampit", "2025-02-20", ["party_pdip"]),
 ("reg_kalsel", "Kalimantan Selatan", "Muhidin", "Q12499404", "M", "1956-05-06", "Binuang", "2025-02-20", ["party_pan"]),
 ("reg_kaltim", "Kalimantan Timur", "Rudy Mas'ud", "Q96988704", "M", "1981-12-07", "Balikpapan", "2025-02-20", ["party_golkar"]),
 ("reg_kaltara", "Kalimantan Utara", "Zainal Arifin Paliwang", "Q107366847", "M", "1962-12-16", "Makassar", "2025-02-20", []),
 ("reg_sulut", "Sulawesi Utara", "Yulius Selvanus", "Q85995331", "M", "", "Tana Toraja", "2025-02-20", []),
 ("reg_sulteng", "Sulawesi Tengah", "Anwar Hafid", "Q25468475", "M", "1968-08-14", "Wosu", "2025-02-20", ["party_demokrat"]),
 ("reg_sulsel", "Sulawesi Selatan", "Andi Sudirman Sulaiman", "Q49252587", "M", "1983-09-25", "Bone", "2025-02-20", []),
 ("reg_sultra", "Sulawesi Tenggara", "Andi Sumangerukka", "Q85988747", "M", "1963-03-11", "Makassar", "2025-02-20", ["party_ppp"]),
 ("reg_gorontalo", "Gorontalo", "Gusnar Ismail", "Q12484981", "M", "1959-12-12", "Gorontalo", "2025-02-20", ["party_demokrat"]),
 ("reg_sulbar", "Sulawesi Barat", "Suhardi Duka", "Q85994583", "M", "1962-05-10", "Mamuju", "2025-02-20", ["party_demokrat"]),
 ("reg_maluku", "Maluku", "Hendrik Lewerissa", "Q96987679", "M", "1968-03-02", "Ambon", "2025-02-20", ["party_gerindra", "party_demokrat"]),
 ("reg_malut", "Maluku Utara", "Sherly Tjoanda", "Q131406018", "F", "1982-08-08", "Ambon", "2025-02-20", ["party_demokrat"]),
 ("reg_papua", "Papua", "Mathius D. Fakhiri", "Q85992784", "M", "1968-01-06", "Manokwari", "2025-10-08", []),
 ("reg_pabar", "Papua Barat", "Dominggus Mandacan", "Q16175168", "M", "1959-12-16", "Manokwari", "2025-02-20", ["party_nasdem"]),
 ("reg_papsel", "Papua Selatan", "Apolo Safanpo", "Q97374063", "M", "1975-04-24", "Asmat", "2025-02-20", []),
 ("reg_papteng", "Papua Tengah", "Meki Fritz Nawipa", "Q132308234", "M", "", "Enarotali", "2025-02-20", []),
 ("reg_pappeg", "Papua Pegunungan", "John Tabo", "Q109437450", "M", "", "", "2025-04-17", []),
 ("reg_pbd", "Papua Barat Daya", "Elisa Kambu", "Q112897422", "M", "1964-03-12", "Ayamaru", "2025-02-20", []),
]
WAHID = ("Abdul Wahid", "Q120221128", "M", "1980-11-21", "Belaras", ["party_pkb"])
SEC = {"Ahmad Luthfi": ("Polri", "retired", "flag"), "Mathius D. Fakhiri": ("Polri", "retired", "flag"),
       "Zainal Arifin Paliwang": ("Polri", "retired", "flag"), "Andi Sumangerukka": ("TNI", "retired", "flag"),
       "Yulius Selvanus": ("TNI", "retired", "flag")}

# organizations: provinces and one local party
have = {o["org_id"] for o in O}
for org, prov, *_ in GOV:
    if org not in have:
        O.append({"org_id": org, "name": f"Pemprov {prov}", "name_long": f"Government of {prov} province",
                  "domain": "regional_government", "org_type": "province"})
if "party_aceh" not in have:
    O.append({"org_id": "party_aceh", "name": "Partai Aceh", "name_long": "Partai Aceh", "domain": "party",
              "org_type": "party", "note": "Local party, contests elections in Aceh only"})

# persons
names, qids = {p["name"]: p for p in P}, {p["wikidata_qid"]: p for p in P if p["wikidata_qid"]}
nxt = max(int(p["person_id"][1:]) for p in P) + 1


def person(name, qid, g, bd, bp):
    global nxt
    if qid in qids or name in names:
        sys.exit(f"{name} is already in persons.csv")
    sec = SEC.get(name, ("", "", ""))
    p = {c: "" for c in P[0]}
    p.update(person_id=f"P{nxt:04d}", name=name, gender=g, birth_date=bd, birth_place=bp,
             partisan_status="not_coded", security_service=sec[0], security_status=sec[1],
             security_rank_band=sec[2], wikidata_qid=qid, bio_src="wikidata")
    nxt += 1
    P.append(p)
    names[name] = p
    return p["person_id"]


def membership(pid, org, role, lvl, basis, start, end, status, src, sid, conf, note):
    M.append({"membership_id": f"M{max(int(m['membership_id'][1:]) for m in M) + 1:04d}", "person_id": pid,
              "org_id": org, "role": role, "role_level": lvl, "basis": basis, "start_date": start, "end_date": end,
              "status_asof": status, "snapshot_layer": "", "in_snapshot": "0", "src": src, "source_id": sid,
              "role_src": "", "role_source_id": "", "confidence": conf, "note": note})


def parties(pid, plist):
    for spec in plist:
        org, s, e = (spec.split(":") + ["", ""])[:3]
        membership(pid, org, "member", "member", "party_affiliation", s, e, "past" if e else "unknown",
                   "wikidata", "S003", "low", "Wikidata P102, not checked against a party source")


for org, prov, name, qid, g, bd, bp, start, plist in GOV:
    pid = person(name, qid, g, bd, bp)
    if org == "reg_riau":
        membership(pid, org, "Pelaksana Tugas Gubernur Riau", "head", "appointed", start, "", "current", "wikipedia",
                   "S009", "high", "vice governor acting as governor since the elected governor was suspended")
    else:
        membership(pid, org, f"Gubernur {prov}", "head", "elected", start, "", "current", "wikipedia", "S009", "high", "")
    parties(pid, plist)
wid = person(*WAHID[:5])
membership(wid, "reg_riau", "Gubernur Riau (nonaktif)", "head", "elected", "2025-02-20", "", "current", "news", "S010", "high",
           "suspended after his arrest by the KPK in November 2025; convicted in July 2026 and on appeal in October 2026, "
           "verdict not final on 13 November 2026")
parties(wid, WAHID[5])

# the four governors already in the dataset now cite the list of sitting governors
for m in M:
    if m["org_id"] in ("reg_jatim", "reg_dki", "reg_jabar", "reg_diy") and m["status_asof"] == "current":
        m.update(src="wikipedia", source_id="S009", confidence="high")
        if m["org_id"] == "reg_diy":
            m["start_date"] = "1998-10-03"

# kinship ties and academy classes from the biographies
pid = {p["name"]: p["person_id"] for p in P}
for a, b, note in [("Joko Widodo", "Bobby Nasution", "father-in-law and son-in-law"),
                   ("Kaesang Pangarep", "Bobby Nasution", "brothers-in-law; Bobby Nasution is married to Kaesang's sister"),
                   ("Amran Sulaiman", "Andi Sudirman Sulaiman", "brothers; Andi Sudirman is the younger")]:
    T.append({"tie_id": f"T{len(T) + 1:03d}", "person_a_id": pid[a], "person_b_id": pid[b], "tie_type": "kinship",
              "note": note, "spec": "main", "start_date": "", "end_date": "", "src": "wikipedia", "source_id": "S011"})
for name, inst, typ, yr in [("Andi Sumangerukka", "Akmil", "military_academy", "1987"),
                            ("Mathius D. Fakhiri", "Akademi Kepolisian", "police_academy", "1990"),
                            ("Ahmad Luthfi", "Sekolah Perwira Militer Sukarela Polri", "police_officer_school", "1989")]:
    E.append({"education_id": f"E{len(E) + 1:03d}", "person_id": pid[name], "institution": inst, "institution_type": typ,
              "level": "officer_commission", "field": "", "grad_year": yr, "country": "ID", "src": "wikipedia",
              "source_id": "S011", "confidence": "high", "note": ""})

write("persons.csv", P)
write("organizations.csv", O)
write("memberships.csv", M)
write("ties.csv", T)
write("education.csv", E)
write("sources.csv", S)
print("persons added:", nxt - 209)

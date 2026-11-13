#!/usr/bin/env python3
"""Version 0.2: recode the governors' party rows, inauguration dates and birth dates from sources beyond Wikidata.

Sources (added to data/sources.csv as S012 to S028): inauguration reports (Galapos list of 20 Feb 2025,
Kompas.id, Setkab), Kompaspedia profiles, the ICW "Kamu Bersih Aku Pilih" candidate profiles, the Gerindra
list of provincial boards, press reports on party moves, and Wikipedia biographies where nothing better was found.
Edits    data/persons.csv, memberships.csv, ties.csv, sources.csv
Run once from the repository root:  python3 scripts/update_governors_sources.py   (stops if S012 exists)
"""
import csv, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1] / "data"
R = "2026-11-13"


def read(n):
    with open(D / n, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write(n, rows):
    with open(D / n, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"{n:16s} {len(rows):4d} rows")


P, O, M, T, S = (read(n) for n in ("persons.csv", "organizations.csv", "memberships.csv", "ties.csv", "sources.csv"))
if any(s["source_id"] == "S012" for s in S):
    sys.exit("already applied")
SRC = [
 ("S012", "news", "Daftar Lengkap Nama Kepala Daerah 2025-2030", "GalaPos ID", "https://galapos.id/2025/02/daftar-lengkap-nama-kepala-daerah-2025.html", "2025-02-21", "Names the 33 governors inaugurated by the president on 20 February 2025"),
 ("S013", "news", "Minister of Home Affairs Inaugurates Governor and Deputy Governor of Aceh Earlier", "Kompas.id", "https://kompas.id/artikel/en-mendagri-lantik-gubernur-dan-wakil-gubernur-aceh-lebih-awal", "2025-02-12", "Muzakir Manaf inaugurated in the Aceh parliament on 12 February 2025"),
 ("S014", "official", "President Prabowo Subianto Inaugurates Governors, Deputy Governors of Papua Mountains, Bangka Belitung Islands", "Sekretariat Kabinet", "https://setkab.go.id/en/president-prabowo-subianto-inaugurates-governors-deputy-governors-of-papua-pegunungan-bangka-belitung-islands", "2025-04-17", "Presidential Decree 39/P of 2025"),
 ("S015", "official", "President Prabowo Inaugurates Papua Governor, Vice Governor", "Sekretariat Kabinet", "https://setkab.go.id/en/president-prabowo-inaugurates-papua-governor-vice-governor", "2025-10-08", "Presidential Decree 108/P of 2025"),
 ("S016", "news", "Ministry Of Home Affairs Appoints Riau Deputy Governor To Replace Governor Abdul Wahid As KPK Suspect", "VOI", "https://voi.id/en/news/530823", "2025-11", "Appointment by ministerial radiogram 100.2.1.3/8861/SJ"),
 ("S017", "profile", "Kompaspedia profiles of governors (Profil Tokoh)", "Kompas", "https://kompaspedia.kompas.id/baca/profil/tokoh/", "", "Birth dates from the Fakta Singkat box, party from the summary and tags; profiles dated 2021 to 2026, read without subscription"),
 ("S018", "profile", "Kamu Bersih Aku Pilih, candidate profiles for the 2024 gubernatorial elections", "Indonesia Corruption Watch", "https://kamubersihakupilih.id/data-pilgub", "", "Birth dates and party background, compiled by ICW from KPU and press sources"),
 ("S019", "official", "Susunan Pengurus DPD - DPC", "Partai Gerindra", "https://gerindra.id/susunan-pengurus-dpd-dpc", "", "Chair and adviser of each provincial board; the page is undated and may lag behind changes"),
 ("S020", "news", "Bobby Nasution Joins Gerindra, PDI-P Touches on the Practical Importance of Power", "Kompas.id", "https://kompas.id/artikel/en-bobby-nasution-gabung-gerindra-pdi-p-singgung-kepentingan-praktis-kekuasaan", "2024-05", "Joined Gerindra on 20 May 2024"),
 ("S021", "news", "Bobby Nasution to run for North Sumatra governor on Gerindra ticket", "The Jakarta Post", "http://thejakartapost.com/indonesia/2024/05/21/bobby-nasution-to-run-for-north-sumatra-governor-on-gerindra-ticket.html", "2024-05-21", "Dismissed by PDI-P in November 2023"),
 ("S022", "news", "Expert: There Is Sudaryono's Role Behind Luthfi-Yasin's Victory In The Central Java Regional Head Election", "VOI", "https://voi.id/en/berita/438042", "", "An analyst states that Ahmad Luthfi has formally become a Gerindra cadre"),
 ("S023", "news", "Gerindra Promotes PDI-P Cadres in Central Kalimantan Regional Election, KIM Does Not Apply in Regions", "Kompas.id", "https://kompas.id/artikel/en-gerindra-usung-kader-pdip-di-pilkada-kalteng-kim-tak-berlaku-di-daerah", "2024", "Agustiar Sabran was a PDI-P member of the DPR when Gerindra nominated him"),
 ("S024", "news", 'West Kalimantan Gubernatorial Election "Exchange", Senior Politicians Fight for Political Party Tickets', "Kompas.id", "https://kompas.id/artikel/en-bursa-pilgub-kalbar-politikus-senior-rebutan-tiket-parpol", "2024", "Ria Norsan described as a Golkar cadre heading the party's council of advisers in West Kalimantan"),
 ("S025", "news", "Profil Rudy Mas'ud, Gubernur Kaltim yang Juluki Dedi Mulyadi \"Gubernur Konten\"", "Kompas.com", "https://kompas.com/kalimantan-timur/read/2025/04/30/075142888/profil-rudy-masud-gubernur-kaltim-yang-juluki-dedi-mulyadi", "2025-04-30", "Chair of DPD Golkar Kalimantan Timur for 2020 to 2025"),
 ("S026", "news", "Riau Golkar Party Regional Conference Schedule Uncertain, Parisman Ihwan Hopes Riau Will Be First", "Halloriau", "https://halloriau.com/read-politik-14606424-2025-04-09-riau-golkar-party-regional-conference-schedule-uncertain-parisman-ihwan-hopes-riau-will-be-first.html", "2025-04-09", "SF Hariyanto named as a Golkar Riau cadre and contender for the provincial chair"),
 ("S027", "encyclopedia", "Wikipedia biographies of the sitting governors (Indonesian and English)", "Wikipedia", "https://id.wikipedia.org/wiki/Daftar_gubernur_dan_wakil_gubernur_di_Indonesia", "", "Used for party rows only where no press, official or profile source was found"),
 ("S028", "news", "KPU Tetapkan Kader PDIP Koster-Giri Pemenang Pilgub Bali", "CNN Indonesia", "https://cnnindonesia.com/nasional/20241208131812-617-1174995/kpu-tetapkan-kader-pdip-koster-giri-pemenang-pilgub-bali", "2024-12-08", ""),
]
for sid, typ, title, pub, url, dp, note in SRC:
    S.append({"source_id": sid, "type": typ, "title": title, "publisher": pub, "url": url, "date_published": dp,
              "date_retrieved": R, "note": note})

pid = {p["name"]: p["person_id"] for p in P}
person = {p["name"]: p for p in P}
dom = {o["org_id"]: o["domain"] for o in O}

# ----------------------------------------------------------- birth dates
BIO = {  # name: (birth_date, birth_place or None to keep, sources)
 "Muzakir Manaf": ("1964-04-03", None, "kompaspedia"), "Bobby Nasution": ("1991-07-05", None, "icw;kompaspedia"),
 "Mahyeldi Ansharullah": ("1966-12-25", None, "icw;kompaspedia"), "SF Hariyanto": ("1965-04-30", None, "icw"),
 "Abdul Wahid": ("1980-11-21", None, "icw;kompaspedia"), "Al Haris": ("1973-11-23", None, "kompaspedia"),
 "Herman Deru": ("1967-11-17", None, "icw;kompaspedia"), "Helmi Hasan": ("1979-11-29", None, "icw"),
 "Rahmat Mirzani Djausal": ("1980-03-18", None, "icw;kompaspedia"), "Hidayat Arsani": ("1963-08-21", None, "icw"),
 "Ansar Ahmad": ("1964-04-10", None, "icw;kompaspedia"), "Ahmad Luthfi": ("1966-11-22", None, "icw;kompaspedia"),
 "Andra Soni": ("1976-08-12", None, "icw;kompaspedia"), "I Wayan Koster": ("1962-10-20", None, "icw;kompaspedia"),
 "Lalu Muhamad Iqbal": ("1972-07-10", None, "icw;kompaspedia"),
 "Emanuel Melkiades Laka Lena": ("1976-12-10", None, "icw;kompaspedia"),
 "Ria Norsan": ("1967-12-17", "Singkawang", "icw;kompaspedia"), "Agustiar Sabran": ("1972-08-17", None, "icw"),
 "Muhidin": ("1958-05-06", None, "icw"), "Rudy Mas'ud": ("1981-12-07", None, "icw"),
 "Zainal Arifin Paliwang": ("1962-12-16", None, "kompaspedia"), "Yulius Selvanus": ("1963-09", None, "icw;kompaspedia"),
 "Anwar Hafid": ("1969-08-14", "Bungku Barat", "kompaspedia"),
 "Andi Sudirman Sulaiman": ("1983-09-25", None, "icw;kompaspedia"),
 "Andi Sumangerukka": ("1963-03-11", None, "icw;kompaspedia"), "Gusnar Ismail": ("1959-12-12", None, "icw;kompaspedia"),
 "Suhardi Duka": ("1962-05-10", None, "icw;kompaspedia"), "Hendrik Lewerissa": ("1968-03-02", None, "icw;kompaspedia"),
 "Sherly Tjoanda": ("1982-08-08", None, "kompaspedia"), "Mathius D. Fakhiri": ("1968-01-06", None, "icw"),
 "Dominggus Mandacan": ("1959-12-16", None, "icw"), "Apolo Safanpo": ("1975-04-24", None, "icw"),
 "Meki Fritz Nawipa": ("1978-05-06", "Enarotali", "icw"), "John Tabo": ("1970-06-02", "Wuragi, Tolikara", "icw"),
 "Elisa Kambu": ("1964-03-12", None, "icw"),
}
changed = []
for name, (bd, bp, src) in BIO.items():
    p = person[name]
    if p["birth_date"] != bd:
        changed.append(f"{name}: {p['birth_date'] or 'empty'} -> {bd}")
    p["birth_date"] = bd
    if bp:
        p["birth_place"] = bp
    p["bio_src"] = src

# ------------------------------------------------- inauguration dates
FEB20 = ["Bobby Nasution", "Mahyeldi Ansharullah", "Al Haris", "Herman Deru", "Helmi Hasan", "Rahmat Mirzani Djausal",
         "Ansar Ahmad", "Pramono Anung", "Dedi Mulyadi", "Andra Soni", "Ahmad Luthfi", "Khofifah Indar Parawansa",
         "I Wayan Koster", "Lalu Muhamad Iqbal", "Emanuel Melkiades Laka Lena", "Ria Norsan", "Agustiar Sabran",
         "Muhidin", "Rudy Mas'ud", "Zainal Arifin Paliwang", "Gusnar Ismail", "Suhardi Duka", "Yulius Selvanus",
         "Anwar Hafid", "Andi Sudirman Sulaiman", "Andi Sumangerukka", "Hendrik Lewerissa", "Sherly Tjoanda",
         "Dominggus Mandacan", "Apolo Safanpo", "Meki Fritz Nawipa", "Elisa Kambu", "Abdul Wahid"]
OTHER = {"Muzakir Manaf": ("2025-02-12", "news", "S013"), "Hidayat Arsani": ("2025-04-17", "official", "S014"),
         "John Tabo": ("2025-04-17", "official", "S014"), "Mathius D. Fakhiri": ("2025-10-08", "official", "S015")}
EARLIER = {"Mahyeldi Ansharullah": "second term; first inaugurated on 25 February 2021 (Kompaspedia)",
           "Zainal Arifin Paliwang": "second term; first inaugurated on 15 February 2021 (Kompaspedia)"}


def gov_row(name):
    rows = [m for m in M if m["person_id"] == pid[name] and dom[m["org_id"]] == "regional_government"
            and m["status_asof"] == "current"]
    if len(rows) != 1:
        sys.exit(f"{name}: {len(rows)} current provincial rows")
    return rows[0]


for name in FEB20:
    m = gov_row(name)
    if m["start_date"] != "2025-02-20":
        sys.exit(f"{name}: start date {m['start_date']}")
    if name == "Abdul Wahid":
        m["role_src"], m["role_source_id"] = "news", "S012"
    else:
        m.update(src="news", source_id="S012", confidence="high")
    if name in EARLIER:
        m["note"] = EARLIER[name]
for name, (d, src, sid) in OTHER.items():
    m = gov_row(name)
    if m["start_date"] != d:
        sys.exit(f"{name}: start date {m['start_date']} differs from {d}")
    m.update(src=src, source_id=sid, confidence="high")
m = gov_row("SF Hariyanto")
m["role_src"], m["role_source_id"] = "news", "S016"
m["note"] = "vice governor appointed acting governor by the home affairs ministry after the elected governor was named a suspect; date from the list of sitting governors"

# -------------------------------------------------------- party rows
new_people = {p["person_id"] for p in P if int(p["person_id"][1:]) >= 209}
M = [m for m in M if not (m["person_id"] in new_people and dom[m["org_id"]] == "party")]
PARTY = [  # name, party, role, role_level, basis, start, end, status, src, source, confidence, note
 ("Muzakir Manaf", "party_aceh", "Ketua Umum", "head", "elected", "", "", "current", "wikipedia", "S027", "medium", "chairs the 2023 to 2028 board"),
 ("Muzakir Manaf", "party_gerindra", "Penasehat DPD Gerindra Aceh", "regional_board", "appointed", "", "", "unknown", "official", "S019", "medium", "on the Gerindra list on 13 November 2026; Wikipedia dates his Gerindra affiliation 2013 to 2022, so the list may be out of date"),
 ("Bobby Nasution", "party_gerindra", "member", "member", "cadre_or_member", "2024-05-20", "", "current", "news", "S020", "high", ""),
 ("Bobby Nasution", "party_pdip", "member", "member", "cadre_or_member", "2020", "2023", "past", "news", "S021", "high", "dismissed in November 2023 after backing Prabowo; start year from Wikidata"),
 ("Mahyeldi Ansharullah", "party_pks", "member", "member", "cadre_or_member", "", "", "current", "profile", "S017", "medium", "nominated by PKS in the 2021 profile; Wikipedia describes him as a PKS politician"),
 ("SF Hariyanto", "party_golkar", "member", "member", "cadre_or_member", "2025", "", "current", "news", "S026", "medium", "career civil servant until 2024; Wikipedia lists PDI-P for 2024 to 2025"),
 ("Abdul Wahid", "party_pkb", "member", "member", "cadre_or_member", "", "", "current", "profile", "S017", "high", "PKB member of the DPR 2019 to 2024"),
 ("Al Haris", "party_pan", "member", "member", "cadre_or_member", "2020", "", "current", "wikipedia", "S027", "medium", "Kompaspedia tags agree"),
 ("Al Haris", "party_golkar", "member", "member", "cadre_or_member", "2013", "2020", "past", "wikipedia", "S027", "low", ""),
 ("Herman Deru", "party_nasdem", "member", "member", "cadre_or_member", "", "", "current", "profile", "S017", "medium", "Ketua DPW NasDem Sumatera Selatan in the 2021 profile; present post not checked"),
 ("Helmi Hasan", "party_pan", "member", "member", "cadre_or_member", "", "", "current", "wikipedia", "S027", "medium", ""),
 ("Rahmat Mirzani Djausal", "party_gerindra", "Ketua DPD Gerindra Lampung", "regional_board", "appointed", "", "", "current", "official", "S019", "high", "confirmed by the 2025 Kompaspedia profile"),
 ("Hidayat Arsani", "party_golkar", "member", "member", "cadre_or_member", "", "", "current", "profile", "S018", "high", "former chair of DPD Golkar Bangka Belitung"),
 ("Ansar Ahmad", "party_golkar", "member", "member", "cadre_or_member", "", "", "current", "profile", "S017", "medium", "from the 2021 profile"),
 ("Ahmad Luthfi", "party_gerindra", "member", "member", "cadre_or_member", "2024", "", "current", "news", "S022", "medium", "Gerindra nominated him in July 2024; cadre status rests on an analyst's statement"),
 ("Andra Soni", "party_gerindra", "Ketua DPD Gerindra Banten", "regional_board", "appointed", "2023", "", "current", "official", "S019", "high", "start year from the ICW profile"),
 ("I Wayan Koster", "party_pdip", "member", "member", "cadre_or_member", "", "", "current", "news", "S028", "high", ""),
 ("Lalu Muhamad Iqbal", "party_gerindra", "member", "member", "cadre_or_member", "2024", "", "current", "wikipedia", "S027", "medium", "career diplomat until 2024; Kompaspedia tags agree"),
 ("Emanuel Melkiades Laka Lena", "party_golkar", "member", "member", "cadre_or_member", "", "", "current", "profile", "S017", "high", ""),
 ("Ria Norsan", "party_gerindra", "member", "member", "cadre_or_member", "2025-04-28", "", "current", "wikipedia", "S027", "medium", "received his membership card from Ahmad Muzani"),
 ("Ria Norsan", "party_golkar", "member", "member", "cadre_or_member", "", "2024", "past", "news", "S024", "medium", "headed Golkar's council of advisers in West Kalimantan in 2024; end year from Wikipedia"),
 ("Agustiar Sabran", "party_gerindra", "member", "member", "cadre_or_member", "2024", "", "current", "wikipedia", "S027", "medium", ""),
 ("Agustiar Sabran", "party_pdip", "member", "member", "cadre_or_member", "", "2024", "past", "news", "S023", "high", "PDI-P member of the DPR 2019 to 2024"),
 ("Muhidin", "party_pan", "member", "member", "cadre_or_member", "", "", "current", "wikipedia", "S027", "medium", ""),
 ("Muhidin", "party_pbr", "member", "member", "cadre_or_member", "", "", "past", "profile", "S018", "medium", "Wikipedia dates this 2002 to 2010"),
 ("Rudy Mas'ud", "party_golkar", "member", "member", "cadre_or_member", "", "", "current", "news", "S025", "high", "Ketua DPD Golkar Kalimantan Timur for the 2020 to 2025 term; successor not checked"),
 ("Zainal Arifin Paliwang", "party_gerindra", "Penasehat DPD Gerindra Kalimantan Utara", "regional_board", "appointed", "", "", "current", "official", "S019", "high", ""),
 ("Yulius Selvanus", "party_gerindra", "Ketua DPD Gerindra Sulawesi Utara", "regional_board", "appointed", "", "", "current", "official", "S019", "high", ""),
 ("Anwar Hafid", "party_demokrat", "member", "member", "cadre_or_member", "", "", "current", "profile", "S017", "high", ""),
 ("Andi Sudirman Sulaiman", "party_gerindra", "member", "member", "party_affiliation", "", "", "unknown", "profile", "S017", "low", "Kompaspedia tags the profile with Gerindra; Wikipedia lists him as independent"),
 ("Andi Sumangerukka", "party_gerindra", "Penasehat DPD Gerindra Sulawesi Tenggara", "regional_board", "appointed", "", "", "current", "official", "S019", "high", ""),
 ("Andi Sumangerukka", "party_ppp", "Ketua DPW PPP Sulawesi Tenggara", "regional_board", "appointed", "2023", "2025", "past", "profile", "S018", "medium", "dates from Wikipedia"),
 ("Gusnar Ismail", "party_demokrat", "member", "member", "cadre_or_member", "", "", "current", "profile", "S017", "medium", ""),
 ("Suhardi Duka", "party_demokrat", "member", "member", "cadre_or_member", "", "", "current", "profile", "S017", "medium", ""),
 ("Hendrik Lewerissa", "party_gerindra", "Ketua DPD Gerindra Maluku", "regional_board", "appointed", "", "", "current", "official", "S019", "high", "confirmed by the ICW profile"),
 ("Mathius D. Fakhiri", "party_golkar", "Ketua DPD Golkar Papua", "regional_board", "elected", "2025-10-17", "", "current", "wikipedia", "S027", "medium", "Wikipedia cites Tribun Papua"),
 ("Dominggus Mandacan", "party_nasdem", "Ketua DPW NasDem Papua Barat", "regional_board", "appointed", "2018", "", "current", "profile", "S018", "high", ""),
 ("Apolo Safanpo", "party_golkar", "member", "member", "party_affiliation", "2025", "", "unknown", "wikipedia", "S027", "low", ""),
 ("Apolo Safanpo", "party_pdip", "member", "member", "party_affiliation", "2024", "2025", "past", "wikipedia", "S027", "low", ""),
 ("Meki Fritz Nawipa", "party_pdip", "member", "member", "cadre_or_member", "", "", "current", "wikipedia", "S027", "medium", ""),
 ("John Tabo", "party_golkar", "member", "member", "cadre_or_member", "", "", "current", "profile", "S018", "high", "Wikipedia names him chair of Golkar in Papua Pegunungan"),
 ("Elisa Kambu", "party_pdip", "member", "member", "cadre_or_member", "", "2024", "past", "profile", "S018", "medium", "end year from Wikipedia"),
 ("Elisa Kambu", "party_gerindra", "member", "member", "party_affiliation", "2025", "", "unknown", "wikipedia", "S027", "low", ""),
]
nxt = max(int(m["membership_id"][1:]) for m in M) + 1
for name, org, role, lvl, basis, s, e, st, src, sid, conf, note in PARTY:
    if dom.get(org) != "party":
        sys.exit(f"unknown party {org}")
    M.append({"membership_id": f"M{nxt:04d}", "person_id": pid[name], "org_id": org, "role": role, "role_level": lvl,
              "basis": basis, "start_date": s, "end_date": e, "status_asof": st, "snapshot_layer": "",
              "in_snapshot": "0", "src": src, "source_id": sid, "role_src": "", "role_source_id": "",
              "confidence": conf, "note": note})
    nxt += 1

# ------------------------------------------------------------- kinship
T.append({"tie_id": f"T{len(T) + 1:03d}", "person_a_id": pid["Zulkifli Hasan"], "person_b_id": pid["Helmi Hasan"],
          "tie_type": "kinship", "note": "brothers; Helmi Hasan is the younger", "spec": "main", "start_date": "",
          "end_date": "", "src": "wikipedia", "source_id": "S027"})

write("persons.csv", P)
write("memberships.csv", M)
write("ties.csv", T)
write("sources.csv", S)
print("birth dates changed:", "; ".join(changed))

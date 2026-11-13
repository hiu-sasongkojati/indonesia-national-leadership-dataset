#!/usr/bin/env python3
"""Add `ethnicity` and `ethnicity_src` to persons.csv.

The values are the ethnic categories that Wikipedia editors attached to each person's article, read through
the MediaWiki API on 13 November 2026 (S051 Indonesian edition, S052 English edition). They record how a
published source describes the person. Nothing was inferred from a name, a birthplace or a religion.
Categories that name a province or a city (Tokoh Lampung, Tokoh Banten, Tokoh Bali, Tokoh Aceh, Tokoh Papua,
Tokoh Maluku, Tokoh Gorontalo, Tokoh Cirebon, Tokoh Bima) were set aside because they mark where a person
comes from. A person with several categories keeps all of them, separated by "; ".
Run once from the repository root:  python3 scripts/add_ethnicity.py
"""
import csv, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1] / "data"
ID, EN = "idwiki", "enwiki"
E = {
    # Indonesian edition
    "Airlangga Hartarto": ("Javanese", ID), "Agum Gumelar": ("Sundanese", ID), "Anis Matta": ("Bugis", ID),
    "Ahmad Heryawan": ("Sundanese", ID), "Anies Baswedan": ("Arab Indonesian; Sundanese", ID),
    "Basuki Tjahaja Purnama": ("Chinese Indonesian", ID), "Budi Gunawan": ("Javanese", ID),
    "Ali Masykur Musa": ("Javanese", ID), "Bambang Soesatyo": ("Javanese", ID), "Bambang Wuryanto": ("Javanese", ID),
    "Bambang Brodjonegoro": ("Javanese", ID), "Bima Arya": ("Sundanese", ID), "Ahmad Sahroni": ("Minangkabau", ID),
    "Ahmad Muzani": ("Javanese", ID), "Amran Sulaiman": ("Bugis", ID), "Agus Andrianto": ("Javanese", ID),
    "Ahmad Doli Kurnia": ("Batak", ID), "Ahmad Ridha Sabana": ("Banjarese; Minangkabau", ID),
    "Ari Dono Sukmanto": ("Javanese; Sundanese", ID), "Budi S. Tanuwibowo": ("Chinese Indonesian", ID),
    "Ace Hasan Syadzily": ("Sundanese", ID), "Abdul Mu'ti": ("Javanese", ID), "Afriansyah Noor": ("Minangkabau", ID),
    "Agus Gumiwang Kartasasmita": ("Sundanese", ID), "Arifatul Choiri Fauzi": ("Madurese", ID),
    "Brian Yuliarto": ("Javanese", ID), "Hidayat Nur Wahid": ("Javanese", ID), "Hatta Rajasa": ("Malay", ID + "+" + EN),
    "Dede Yusuf": ("Minangkabau; Sundanese", ID), "GKR Hemas": ("Javanese", ID), "Dedi Mulyadi": ("Sundanese", ID),
    "Grace Natalie": ("Chinese Indonesian; Malay", ID), "Jeffrie Geovanie": ("Minangkabau", ID),
    "Fadli Zon": ("Minangkabau", ID), "Erick Thohir": ("Chinese Indonesian", ID),
    "Edhie Baskoro Yudhoyono": ("Javanese", ID), "Chatib Basri": ("Minangkabau", ID),
    "Ignasius Jonan": ("Chinese Indonesian", ID), "Hashim Djojohadikusumo": ("Javanese", ID),
    "Condro Kirono": ("Javanese", ID), "Hanif Dhakiri": ("Javanese", ID), "Ida Fauziyah": ("Javanese", ID),
    "Djarot Saiful Hidayat": ("Javanese", ID), "Dony Oskaria": ("Minangkabau", ID),
    "Dudung Abdurachman": ("Sundanese", ID), "Erwin Aksa": ("Bugis", ID), "Hasanuddin Wahid": ("Javanese", ID),
    "Deddy Sitorus": ("Batak", ID), "Hermawi Taslim": ("Chinese Indonesian", ID), "Hasan Nasbi": ("Minangkabau", ID),
    "Dody Hanggodo": ("Javanese", ID), "Hinca Pandjaitan": ("Batak", ID),
    "Megawati Soekarnoputri": ("Javanese; Minangkabau; Balinese", ID + "+" + EN), "Meutya Hafid": ("Bugis", ID),
    "Quraish Shihab": ("Arab Indonesian; Indian Indonesian; Bugis", ID), "Joko Widodo": ("Javanese", ID),
    "Mari Elka Pangestu": ("Chinese Indonesian", ID), "Purnomo Yusgiantoro": ("Javanese", ID),
    "Khofifah Indar Parawansa": ("Javanese", ID), "Luhut Binsar Pandjaitan": ("Batak", ID),
    "Mahfud MD": ("Madurese", ID), "Jusuf Wanandi": ("Chinese Indonesian", ID),
    "Prabowo Subianto": ("Javanese; Minahasan", ID), "Ma'ruf Amin": ("Arab Indonesian; Javanese; Sundanese", ID),
    "Pramono Anung": ("Javanese", ID), "Muhaimin Iskandar": ("Javanese", ID),
    "Puan Maharani": ("Javanese; Minangkabau", ID), "Pratikno": ("Javanese", ID),
    "Muhammad Herindra": ("Javanese", ID), "Nusron Wahid": ("Javanese", ID), "Maruli Simanjuntak": ("Batak", ID),
    "Maruarar Sirait": ("Batak", ID), "M. Sarmuji": ("Javanese", ID),
    "Raja Juli Antoni": ("Malay; Minangkabau", ID + "+" + EN), "Olly Dondokambey": ("Minahasan", ID),
    "Muhadjir Effendy": ("Javanese", ID), "Lestari Moerdijat": ("Javanese", ID),
    "Jusuf Hamka": ("Chinese Indonesian", ID), "Prasetyo Hadi": ("Javanese", ID),
    "Susilo Bambang Yudhoyono": ("Javanese", ID), "Wiranto": ("Javanese", ID), "Saifullah Yusuf": ("Javanese", ID),
    "Sultan Hamengku Buwono X": ("Javanese", ID), "Sinta Nuriyah Wahid": ("Javanese", ID), "Soekarwo": ("Javanese", ID),
    "Sjafrie Sjamsoeddin": ("Bugis", ID), "Salim Segaf Al-Jufri": ("Arab Indonesian", ID),
    "Willy Aditya": ("Minangkabau", ID), "Said Abdullah": ("Madurese", ID), "Rosan Roeslani": ("Betawi", ID),
    "Tandyo Budi Revita": ("Javanese", ID), "Suyudi Ario Seto": ("Javanese", ID), "Wihaji": ("Javanese", ID),
    "Thomas Djiwandono": ("Javanese", ID), "Terawan Agus Putranto": ("Javanese", ID),
    "ST Burhanuddin": ("Sundanese", ID), "Suahasil Nazara": ("Nias", ID), "Sakti Wahyu Trenggono": ("Javanese", ID),
    "Yahya Cholil Staquf": ("Javanese", ID), "Teddy Indra Wijaya": ("Javanese", ID),
    "Widiyanti Putri": ("Javanese", ID), "Wahyu Hadiningrat": ("Sundanese", ID),
    "Yusril Ihza Mahendra": ("Malay; Minangkabau", ID), "Saleh Daulay": ("Batak", ID), "Yasonna Laoly": ("Nias", ID),
    "Muhidin": ("Banjarese", ID), "Yorrys Raweyai": ("Chinese Indonesian", ID),
    "Mahyeldi Ansharullah": ("Minangkabau", ID), "Hidayat Arsani": ("Chinese Indonesian", ID),
    "Yovianes Mahar": ("Minangkabau", ID), "Agustiar Sabran": ("Dayak", ID),
    "Andi Sudirman Sulaiman": ("Bugis", ID), "Suhardi Duka": ("Mandarese", ID), "Lalu Muhamad Iqbal": ("Sasak", ID),
    "Yulius Selvanus": ("Minahasan; Torajan", ID), "Andi Sumangerukka": ("Bugis", ID), "Andra Soni": ("Minangkabau", ID),
    "Yassierli": ("Minangkabau", ID + "+" + EN), "Sherly Tjoanda": ("Chinese Indonesian", ID),
    # English edition only
    "Chairul Tanjung": ("Minangkabau; Sundanese", EN), "Cucun Ahmad Syamsurijal": ("Sundanese", EN),
    "Kaesang Pangarep": ("Javanese", EN), "Tito Karnavian": ("Malay", EN), "Rusdi Kirana": ("Chinese Indonesian", EN),
    "Pandu Sjahrir": ("Batak; Minangkabau", EN), "Lodewijk F. Paulus": ("Indo", EN), "Said Iqbal": ("Acehnese", EN),
    "Rocky Gerung": ("Minahasan", EN), "Tahir": ("Chinese Indonesian", EN), "Zulkifli Hasan": ("Lampung", EN),
    "Helmi Hasan": ("Lampung", EN), "I Wayan Koster": ("Balinese", EN), "Bobby Nasution": ("Batak", EN),
    "Dominggus Mandacan": ("Papuan", EN), "Apolo Safanpo": ("Papuan", EN),
}


def read(n):
    with open(D / n, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write(n, rows, cols):
    with open(D / n, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, cols, quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


P, S = read("persons.csv"), read("sources.csv")
if "ethnicity" in P[0]:
    sys.exit("already applied")
names = {p["name"] for p in P}
missing = set(E) - names
assert not missing, missing
cols = list(P[0])
i = cols.index("religion") + 1
cols[i:i] = ["ethnicity", "ethnicity_src"]
for p in P:
    p["ethnicity"], p["ethnicity_src"] = E.get(p["name"], ("", ""))
for sid, title, url in (
        ("S051", "Ethnic categories on biographies in the Indonesian Wikipedia (Tokoh Jawa, Tokoh Sunda, Politikus Minangkabau and others)",
         "https://id.wikipedia.org/w/api.php"),
        ("S052", "Ethnic categories on biographies in the English Wikipedia (Javanese people, People of Batak descent and others)",
         "https://en.wikipedia.org/w/api.php")):
    S.append({"source_id": sid, "type": "encyclopedia", "title": title, "publisher": "Wikipedia", "url": url,
              "date_published": "", "date_retrieved": "2026-11-13",
              "note": "Read through the MediaWiki API (prop=categories) with a filter of 50 category names"})
write("persons.csv", P, cols)
write("sources.csv", S, list(S[0]))
print(sum(bool(p["ethnicity"]) for p in P), "of", len(P), "people coded")

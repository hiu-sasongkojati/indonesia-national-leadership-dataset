#!/usr/bin/env python3
"""Add organisation posts and company seats from published boards (version 0.2.0).

Part 1 codes posts in religious, student, professional and business organisations from the boards those
organisations published, or from press reports of them. Part 2 adds a `company` domain: seats on the boards
of listed companies, direct shareholdings, and holding companies that the press attributes to a person.
The company rows come from a sweep of the management and shareholder lists of all 964 companies on the
Indonesia Stock Exchange as shown by IDNFinancials on 13 November 2026, matched by name.
Run once from the repository root:  python3 scripts/add_boards_companies.py
"""
import csv, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1] / "data"
TODAY = "2026-11-13"


def read(n):
    with open(D / n, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write(n, rows):
    with open(D / n, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, list(rows[0]), quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


P, O, M, S = read("persons.csv"), read("organizations.csv"), read("memberships.csv"), read("sources.csv")
if any(s["source_id"] == "S030" for s in S):
    sys.exit("already applied")
pid = {p["name"]: p["person_id"] for p in P}

SOURCES = [
    ("S030", "official", "Susunan Lengkap Kepengurusan PBNU Masa Khidmah 2026-2031", "NU Online",
     "https://nu.or.id/nasional/susunan-lengkap-kepengurusan-pbnu-masa-khidmah-2026-2031-bgMjP", "2026-09-30",
     "Board set by decree of 30 September 2026 after the 35th Muktamar"),
    ("S031", "news", "PBNU Rilis Pengurus Baru Masa Khidmat 2022-2027, Berikut Susunannya", "RMOL Jabar",
     "https://rmoljabar.id/pbnu-rilis-pengurus-baru-masa-khidmat-2022-2027-berikut-susunannya", "2022-01-12",
     "The page shows the Mustasyar, Syuriyah and A'wan lists; the Tanfidziyah list was not retrieved"),
    ("S032", "news", "Lengkap! Ini Susunan Kepengurusan MUI Periode 2025-2030", "Metro TV News",
     "https://www.metrotvnews.com/read/NP6C3xWL-lengkap-ini-susunan-kepengurusan-mui-periode-2025-2030", "2025-11",
     "Reproduces the list on the MUI website after the 11th Munas of 20 to 22 November 2025"),
    ("S033", "official", "Here Is the Composition of the Central Executive Board of Muhammadiyah for the 2022-2027 Period",
     "Muhammadiyah", "https://en.muhammadiyah.or.id/70597-2", "", ""),
    ("S034", "official", "Struktur Organisasi Kadin Indonesia", "KADIN Indonesia",
     "https://kadin.id/struktur-organisasi-kadin", "", "Board of the 2024-2029 term as displayed on the retrieval date"),
    ("S035", "news", "9 Anggota Presidium MN KAHMI Terpilih, 7 Orang Parpol", "SINDOnews",
     "https://nasional.sindonews.com/read/953029/12/9-anggota-presidium-mn-kahmi-terpilih-7-orang-parpol-1669511515",
     "2022-11-27", ""),
    ("S036", "news", "Deretan Tokoh Nasional Perkuat Kepengurusan Pusat MES 1447-1452 H", "Bacaini.id",
     "https://bacaini.id/deretan-tokoh-nasional-perkuat-kepengurusan-pusat-mes-1447-1452-h/", "2026-02",
     "Reports decree 001/SK/MES-PST/II/2026 of 10 February 2026; names a selection of each council"),
    ("S037", "news", "Khofifah Continues To Lead NU Muslimat For The 2025-2030 Period", "VOI",
     "https://voi.id/en/news/460317", "2025-02", "Cites Antara"),
    ("S038", "news", "Indonesian women urged to support national development through family", "Antara",
     "https://en.antaranews.com/news/412003/homepage-v2.html", "", "Describes the minister as chair of Muslimat NU"),
    ("S039", "news", "Sudaryono takes helm at HKTI", "Antara", "https://en.antaranews.com/news/362313/sudaryono-takes-helm-at-hkti",
     "2025-06-26", ""),
    ("S040", "news", "Appointed As HKTI Chair, Deputy Minister Sudaryono Affirms Pursuit Of Food Swasembada Targets", "VOI",
     "https://voi.id/en/economy/490833", "2025-06", "Gives the earlier chairs of both HKTI factions"),
    ("S041", "news", "KONI Serahkan SK Kepengurusan IMI 2025-2030, Moreno Soeprapto Siap Gaspol", "One News",
     "https://one.news/en/artikel/40209/koni-serahkan-sk-kepengurusan-imi-20252030-moreno-soeprapto-siap-gaspol", "2025-10", ""),
    ("S042", "news", "Munas XVIII HIPMI Tetapkan Ade Jona Prasetyo sebagai Ketua Umum Baru", "MataKita",
     "https://matakita.co/2026/06/11/munas-xviii-hipmi-tetapkan-ade-jona-prasetyo-sebagai-ketua-umum-baru", "2026-06-11", ""),
    ("S043", "official", "BPP HIPMI Instagram post naming the Ketua Dewan Kehormatan", "BPP HIPMI",
     "https://instagram.com/reel/DVF8JoEAWzn", "2026-02", "Read through the search snippet; the reel was not opened"),
    ("S044", "encyclopedia", "Wikipedia articles on organisations (DMI, PGI, PA GMNI, Fatayat NU, HKTI, HIPMI, PSSI, KSPSI, KSPI, KNPI)",
     "Wikipedia", "https://id.wikipedia.org/wiki/Dewan_Masjid_Indonesia", "", "Indonesian edition, read through the MediaWiki API"),
    ("S045", "market_data", "Company pages: management and shareholders of companies listed on the Indonesia Stock Exchange",
     "IDNFinancials", "https://www.idnfinancials.com/company", "",
     "All 964 listed companies swept on the retrieval date; seven tickers returned no data (JECX, RANS, EMMI, BACH, JELI, PRDL, KBRI). "
     "Shareholder figures carry their own reporting date"),
    ("S046", "official", "Arsari Group website", "Arsari Group", "https://www.arsari.co.id/", "", ""),
    ("S047", "news", "TBS Energi Utama shifts focus to non-coal business", "Indonesia Business Post",
     "https://indonesiabusinesspost.com/983/business-and-investment/tbs-energi-utama-shifts-focus-to-non-coal-business", "2023", ""),
    ("S048", "news", "Mundur dari Mahaka, Posisi Erick Thohir Diganti Harry Zulnardy", "Tempo",
     "https://tempo.co/politik/mundur-dari-mahaka-posisi-erick-thohir-diganti-harry-zulnardy-674407", "2019-12", ""),
    ("S049", "news", "Mahaka Media to divest shares in CRM company", "IDNFinancials",
     "https://idnfinancials.com/news/50200/mahaka-media-divest-shares-crm-company", "", "Calls Erick Thohir the owner of the parent entity"),
    ("S050", "news", "Kaesang-Affiliated PMMP Saddled with Debt, Cuts Jobs", "Tempo",
     "https://en.tempo.co/read/2112827/kaesang-affiliated-pmmp-saddled-with-debt-cuts-jobs", "2026", ""),
]
for sid, typ, title, pub, url, date, note in SOURCES:
    S.append({"source_id": sid, "type": typ, "title": title, "publisher": pub, "url": url, "date_published": date,
              "date_retrieved": TODAY, "note": note})

ORGS = [
    # org_id, name, name_long, domain, org_type, stream, note
    ("ormas_mes", "MES", "Masyarakat Ekonomi Syariah", "mass_organization", "religious_economic_society", "Islam", ""),
    ("ormas_dmi", "DMI", "Dewan Masjid Indonesia", "mass_organization", "religious_council", "Islam", ""),
    ("ormas_hkti", "HKTI", "Himpunan Kerukunan Tani Indonesia", "mass_organization", "farmers_association", "",
     "Two rival boards from 2010 until the congress of June 2025"),
    ("ormas_pa_gmni", "PA GMNI", "Persatuan Alumni Gerakan Mahasiswa Nasional Indonesia", "mass_organization", "student_alumni",
     "nationalist", ""),
    ("soe_jsmr", "Jasa Marga (JSMR)", "PT Jasa Marga (Persero) Tbk", "state_enterprise", "listed_state_enterprise", "", ""),
    ("soe_bris", "Bank Syariah Indonesia (BRIS)", "PT Bank Syariah Indonesia (Persero) Tbk", "state_enterprise",
     "listed_state_enterprise", "", ""),
    ("co_asii", "Astra International (ASII)", "PT Astra International Tbk", "company", "listed_company", "", ""),
    ("co_untr", "United Tractors (UNTR)", "PT United Tractors Tbk", "company", "listed_company", "", ""),
    ("co_soho", "Soho Global Health (SOHO)", "PT Soho Global Health Tbk", "company", "listed_company", "", ""),
    ("co_silo", "Siloam Hospitals (SILO)", "PT Siloam International Hospitals Tbk", "company", "listed_company", "", ""),
    ("co_lpkr", "Lippo Karawaci (LPKR)", "PT Lippo Karawaci Tbk", "company", "listed_company", "", ""),
    ("co_indy", "Indika Energy (INDY)", "PT Indika Energy Tbk", "company", "listed_company", "",
     "PT Indika Inti Investindo held 37.84% and PT Teladan Resources 28.12% on 30 June 2026"),
    ("co_tldn", "Teladan Prima Agro (TLDN)", "PT Teladan Prima Agro Tbk", "company", "listed_company", "",
     "PT Teladan Resources held 59.89% on 31 December 2025"),
    ("co_aali", "Astra Agro Lestari (AALI)", "PT Astra Agro Lestari Tbk", "company", "listed_company", "", ""),
    ("co_mega", "Bank Mega (MEGA)", "PT Bank Mega Tbk", "company", "listed_company", "",
     "PT Mega Corpora held 58.02% on 30 June 2026; it also held 60.88% of Allo Bank (BBHI)"),
    ("co_maya", "Bank Mayapada (MAYA)", "PT Bank Mayapada Internasional Tbk", "company", "listed_company", "",
     "PT Mayapada Karunia held 24.16% and PT Mayapada Kasih 12.31% on 30 June 2026, both share series combined"),
    ("co_sona", "Sona Topas Tourism (SONA)", "PT Sona Topas Tourism Industry Tbk", "company", "listed_company", "", ""),
    ("co_imas", "Indomobil (IMAS)", "PT Indomobil Sukses Internasional Tbk", "company", "listed_company", "", ""),
    ("co_cmnp", "Citra Marga Nusaphala Persada (CMNP)", "PT Citra Marga Nusaphala Persada Tbk", "company", "listed_company", "", ""),
    ("co_tspc", "Tempo Scan Pacific (TSPC)", "PT Tempo Scan Pacific Tbk", "company", "listed_company", "", ""),
    ("co_mknt", "Mitra Komunikasi Nusantara (MKNT)", "PT Mitra Komunikasi Nusantara Tbk", "company", "listed_company", "", ""),
    ("co_vici", "Victoria Care Indonesia (VICI)", "PT Victoria Care Indonesia Tbk", "company", "listed_company", "", ""),
    ("co_trin", "Perintis Triniti Properti (TRIN)", "PT Perintis Triniti Properti Tbk", "company", "listed_company", "", ""),
    ("co_nest", "Esta Indonesia (NEST)", "PT Esta Indonesia Tbk", "company", "listed_company", "", ""),
    ("co_ahap", "Asuransi Harta Aman Pratama (AHAP)", "PT Asuransi Harta Aman Pratama Tbk", "company", "listed_company", "", ""),
    ("co_abba", "Mahaka Media (ABBA)", "PT Mahaka Media Tbk", "company", "listed_company", "",
     "PT Beyond Media held 40.47% on 30 September 2024"),
    ("co_mari", "Mahaka Radio Integra (MARI)", "PT Mahaka Radio Integra Tbk", "company", "listed_company", "",
     "PT Beyond Media held 40.35% and PT Mahaka Media 16.37% on 30 September 2024"),
    ("co_beyond_media", "Beyond Media", "PT Beyond Media", "company", "holding_company", "", "Largest shareholder of Mahaka Media"),
    ("co_toba_sejahtra", "Toba Sejahtra", "PT Toba Sejahtra", "company", "holding_company", "",
     "Held 7.92% of PT TBS Energi Utama Tbk (TOBA) on 30 June 2026; Highland Strategic Holdings held 59.91%"),
    ("co_hbk", "Harapan Bangsa Kita", "PT Harapan Bangsa Kita", "company", "holding_company", "",
     "Held 7.27% of PT Panca Mitra Multiperdana Tbk (PMMP) on 30 June 2025"),
    ("co_arsari", "Arsari Group", "Arsari Group", "company", "private_group", "", ""),
]
for oid, name, long, dom, typ, stream, note in ORGS:
    O.append({"org_id": oid, "name": name, "name_long": long, "domain": dom, "org_type": typ, "parent_org_id": "",
              "stream": stream, "snapshot_name": "", "note": note})

# ---- changes to rows already in the table
by_id = {m["membership_id"]: m for m in M}


def upd(mid, **kw):
    by_id[mid].update(kw)


upd("M0313", start_date="2021-12", end_date="2026", status_asof="past", src="official", source_id="S030", confidence="high",
    note="Elected at the 34th Muktamar in December 2021; the board of September 2026 names a new chair")
upd("M0319", start_date="2022-01", end_date="2026", status_asof="past", src="news", source_id="S031", confidence="medium",
    note="End year is the date of the next board; the PBNU dispute of late 2025 may have ended the post earlier")
upd("M0317", status_asof="current", src="news", source_id="S032", confidence="high", note="Re-elected for 2025-2030 in November 2025")
upd("M0325", end_date="2025-02", status_asof="past", src="news", source_id="S037",
    note="Moved to the chair of the Dewan Pembina at the congress of February 2025")
upd("M0327", src="official", source_id="S033", note="Listed for 2022-2027; start year from background knowledge")
upd("M0328", src="official", source_id="S033", confidence="high",
    note="Listed for 2022-2027 with the economy, business and halal industry portfolio; start year from background knowledge")
upd("M0339", start_date="2022-11", end_date="2026-06", status_asof="past", src="news", source_id="S042", confidence="high",
    note="Elected 23 November 2022; succeeded at the congress of 11 June 2026")
upd("M0338", src="wikipedia", source_id="S044")
upd("M0341", start_date="2023-02", src="wikipedia", source_id="S044", note="Elected 16 February 2023 for a term to 2027")
upd("M0342", src="wikipedia", source_id="S044")
upd("M0343", src="wikipedia", source_id="S044", note="Leadership contested with a rival board under Yorrys Raweyai")
upd("M0345", end_date="2025", status_asof="past", src="news", source_id="S041", confidence="medium",
    note="KONI confirmed a new chair for 2025-2030 in October 2025")
upd("M0326", src="wikipedia", source_id="S044")
upd("M0330", src="wikipedia", source_id="S044", note="Board of 2024-2029")

# ---- new rows
n = max(int(m["membership_id"][1:]) for m in M)
LEVEL = {"H": "head", "D": "deputy_head", "E": "executive_board", "C": "council", "N": "not_coded"}


def add(person, org, role, level, basis, start="", end="", status="current", src="official", sid="", conf="high", note=""):
    global n
    n += 1
    M.append({"membership_id": f"M{n:04d}", "person_id": pid[person], "org_id": org, "role": role,
              "role_level": LEVEL[level], "basis": basis, "start_date": start, "end_date": end, "status_asof": status,
              "snapshot_layer": "", "in_snapshot": "0", "src": src, "source_id": sid, "role_src": "",
              "role_source_id": "", "confidence": conf, "note": note})


BOTH = "Also on the 2022-2027 board (S031)"
# PBNU, board of 2026-2031 (S030) and of 2022-2027 (S031)
for who in ("Ma'ruf Amin", "Said Aqil Siradj", "Sinta Nuriyah Wahid"):
    add(who, "ormas_nu", "Mustasyar PBNU", "C", "appointed", "2022-01", sid="S030", note=BOTH)
add("Mahfud MD", "ormas_nu", "Mustasyar PBNU", "C", "appointed", "2026-09", sid="S030")
add("Irfan Yusuf", "ormas_nu", "Mustasyar PBNU", "C", "appointed", "2026-09", sid="S030", conf="medium",
    note="Listed as KH Irfan Yusuf")
add("Herman Deru", "ormas_nu", "Mustasyar PBNU", "C", "appointed", "2022-01", "2026", "past", "news", "S031", "medium")
for who in ("Khofifah Indar Parawansa", "Nusron Wahid"):
    add(who, "ormas_nu", "A'wan PBNU", "C", "appointed", "2026-09", sid="S030")
for who in ("Herman Deru", "Agustiar Sabran"):
    add(who, "ormas_nu", "A'wan PBNU", "C", "appointed", "2026-09", sid="S030", conf="medium", note="Identified by name")
add("Ali Masykur Musa", "ormas_nu", "A'wan PBNU", "C", "appointed", "2022-01", "2026", "past", "news", "S031", "medium")
add("Anwar Iskandar", "ormas_nu", "Wakil Rais Aam PBNU", "D", "appointed", "2022-01", sid="S030", note=BOTH)
add("Nasaruddin Umar", "ormas_nu", "Rais Syuriyah PBNU", "E", "appointed", "2022-01", sid="S030", note=BOTH)
add("Saifullah Yusuf", "ormas_nu", "Wakil Ketua Umum PBNU", "D", "appointed", "2026-09", sid="S030")
add("Juri Ardiantoro", "ormas_nu", "Wakil Ketua Umum PBNU", "D", "appointed", "2026-09", sid="S030")
# MUI 2025-2030 (S032)
add("Ma'ruf Amin", "ormas_mui", "Ketua Dewan Pertimbangan", "C", "appointed", "2020", src="news", sid="S032",
    note="Returned to the post in November 2025; start year from background knowledge")
for who in ("Nasaruddin Umar", "Tamsil Linrung"):
    add(who, "ormas_mui", "Wakil Ketua Dewan Pertimbangan", "C", "appointed", "2025-11", src="news", sid="S032")
add("Nusron Wahid", "ormas_mui", "Ketua Bidang Penanggulangan Bencana", "E", "appointed", "2025-11", src="news", sid="S032")
add("Rudy Mas'ud", "ormas_mui", "Bendahara", "E", "appointed", "2025-11", src="news", sid="S032", conf="medium",
    note="Listed as Rudi Mas'ud; identified by name")
# KADIN 2024-2029 (S034)
add("Erwin Aksa", "biz_kadin", "Wakil Ketua Umum Koordinator Bidang Organisasi, Komunikasi dan Pemberdayaan Daerah", "E",
    "appointed", sid="S034")
add("Bambang Soesatyo", "biz_kadin", "Wakil Ketua Umum Koordinator Bidang Politik dan Keamanan", "E", "appointed", sid="S034")
add("Rahayu Saraswati", "biz_kadin", "Wakil Ketua Umum Bidang Kebudayaan", "E", "appointed", sid="S034")
add("Rosan Roeslani", "biz_kadin", "Ketua Dewan Kehormatan", "C", "appointed", sid="S034")
add("Chairul Tanjung", "biz_kadin", "Ketua Dewan Usaha", "C", "appointed", sid="S034")
add("Hashim Djojohadikusumo", "biz_kadin", "Ketua Dewan Penasihat", "C", "appointed", sid="S034")
# KAHMI presidium 2022-2027 (S035)
for who in ("Ahmad Doli Kurnia", "Herman Khaeron", "Saan Mustopa"):
    add(who, "ormas_kahmi", "Presidium Majelis Nasional KAHMI", "E", "elected", "2022-11", src="news", sid="S035",
        note="One of nine presidium members elected for 2022-2027")
# MES 1447-1452 H (S036)
add("Rosan Roeslani", "ormas_mes", "Ketua Umum", "H", "elected", "2026-02", src="news", sid="S036",
    note="Start date is that of the board decree")
add("Ferry Juliantono", "ormas_mes", "Ketua Harian", "D", "appointed", "2026-02", src="news", sid="S036")
add("Muliaman Hadad", "ormas_mes", "Ketua Dewan Pembina", "C", "appointed", "2026-02", src="news", sid="S036")
add("Erick Thohir", "ormas_mes", "Wakil Ketua Dewan Pembina", "C", "appointed", "2026-02", src="news", sid="S036")
add("Nasaruddin Umar", "ormas_mes", "Anggota Dewan Pembina", "C", "appointed", "2026-02", src="news", sid="S036")
add("Ma'ruf Amin", "ormas_mes", "Ketua Dewan Pertimbangan", "C", "appointed", "2026-02", src="news", sid="S036")
add("Prasetyo Hadi", "ormas_mes", "Anggota Dewan Pertimbangan", "C", "appointed", "2026-02", src="news", sid="S036")
for who in ("Bahlil Lahadalia", "Irfan Yusuf", "Muhammad Qodari"):
    add(who, "ormas_mes", "Anggota Dewan Penggerak", "C", "appointed", "2026-02", src="news", sid="S036")
for who in ("Pandu Sjahrir", "Dony Oskaria"):
    add(who, "ormas_mes", "Anggota Dewan Penyantun", "C", "appointed", "2026-02", src="news", sid="S036")
# Muslimat NU 2025-2030 (S037, S038)
add("Khofifah Indar Parawansa", "ormas_nu_muslimat", "Ketua Umum Dewan Pembina PP Muslimat NU", "C", "elected", "2025-02",
    src="news", sid="S037")
add("Arifatul Choiri Fauzi", "ormas_nu_muslimat", "Ketua Umum PP Muslimat NU", "H", "elected", "2025-02", src="news", sid="S038",
    note="Start date is that of the congress of February 2025")
# HKTI (S039, S040, S044)
add("Sudaryono", "ormas_hkti", "Ketua Umum DPN HKTI", "H", "elected", "2025-06", src="news", sid="S039")
add("Fadli Zon", "ormas_hkti", "Ketua Umum DPN HKTI", "H", "elected", "2015", "2025-06", "past", "news", "S040",
    note="Chair of the board that descended from the Prabowo faction")
add("Prabowo Subianto", "ormas_hkti", "Ketua Umum HKTI", "H", "elected", "2004", "2015", "past", "wikipedia", "S044", "medium",
    note="A rival board existed from 2010")
# DMI 2024-2029, PGI 2024-2029, PA GMNI and other chairs from Wikipedia (S044)
add("Nasaruddin Umar", "ormas_dmi", "Wakil Ketua Majelis Mustasyar", "C", "appointed", "2024", src="wikipedia", sid="S044", conf="medium")
for who in ("Ahmad Muzani", "Chairul Tanjung"):
    add(who, "ormas_dmi", "Anggota Majelis Mustasyar", "C", "appointed", "2024", src="wikipedia", sid="S044", conf="medium")
add("Olly Dondokambey", "ormas_pgi", "Ketua MPH PGI", "E", "elected", "2024", src="wikipedia", sid="S044", conf="medium")
add("Ahmad Basarah", "ormas_pa_gmni", "Ketua Umum PA GMNI", "H", "elected", "2015", "2020", "past", "wikipedia", "S044", "medium")
add("Soekarwo", "ormas_pa_gmni", "Ketua Umum PA GMNI", "H", "elected", "2010", "2015", "past", "wikipedia", "S044", "medium")
add("Yorrys Raweyai", "ormas_kspsi", "Ketua Umum (rival board)", "H", "elected", status="unknown", src="wikipedia", sid="S044",
    conf="medium", note="Leadership contested with the board under Jumhur Hidayat")
add("Agum Gumelar", "ormas_pssi", "Ketua Umum", "H", "elected", status="past", src="wikipedia", sid="S044", conf="medium",
    note="Dates not given in the source")
add("Agum Gumelar", "ormas_pssi", "Ketua Komite Normalisasi", "H", "appointed", "2011", "2011", "past", "wikipedia", "S044", "medium")
add("Hinca Pandjaitan", "ormas_pssi", "Wakil Ketua Umum", "D", "elected", status="past", src="wikipedia", sid="S044", conf="medium",
    note="Dates not given in the source")
add("Idrus Marham", "ormas_knpi", "Ketua Umum", "H", "elected", status="past", src="wikipedia", sid="S044", conf="medium",
    note="Elected after 1998; dates not given in the source")
add("Bahlil Lahadalia", "biz_hipmi", "Ketua Dewan Kehormatan BPP HIPMI", "C", "appointed", sid="S043", conf="medium",
    note="As described by BPP HIPMI in February 2026")

# ---- companies and listed state enterprises (S045 unless stated)
NM = "Identified by name in the company listing"


def board(person, org, role, level, conf="medium", note=NM):
    add(person, org, role, level, "appointed", src="idnfinancials", sid="S045", conf=conf, note=note)


def stake(person, org, pct, date, conf="medium", note=NM):
    add(person, org, f"Shareholder, {pct}% ({date})", "N", "owner", src="idnfinancials", sid="S045", conf=conf, note=note)


board("Muliaman Hadad", "co_asii", "Independent Commissioner", "C")
board("Chatib Basri", "co_asii", "Independent Commissioner and Chairman of the Audit Committee", "C")
board("Ignasius Jonan", "co_untr", "Chairman of the Audit Committee", "C",
      note="Listed for the audit committee only, not among the commissioners")
board("Ignasius Jonan", "co_soho", "President Commissioner", "C")
board("Yasonna Laoly", "co_silo", "President Commissioner", "C")
board("Bambang Soesatyo", "co_silo", "Independent Commissioner", "C")
board("Bambang Soesatyo", "co_lpkr", "Independent Commissioner", "C")
board("Wishnu Wardhana", "co_indy", "Vice President Commissioner", "C", "high", "")
stake("Wishnu Wardhana", "co_indy", "0.09", "30 Jun 2026", "high", "")
board("Wishnu Wardhana", "co_tldn", "President Director", "H", "high", "")
stake("Wishnu Wardhana", "co_tldn", "16.22", "31 Dec 2025", "high", "")
board("Ari Dono Sukmanto", "co_aali", "Independent Commissioner", "C")
board("Juri Ardiantoro", "soe_jsmr", "President Commissioner", "C")
board("Muhadjir Effendy", "soe_bris", "President Commissioner", "C")
board("Chairul Tanjung", "co_mega", "President Commissioner", "C", "high", "Holding company stake is in the organisation note")
board("Tahir", "co_maya", "President Commissioner", "C", "high", "Holding company stakes are in the organisation note")
stake("Tahir", "co_sona", "15.7", "31 Dec 2025")
board("Jusuf Hamka", "co_imas", "Independent Commissioner", "C")
stake("Jusuf Hamka", "co_cmnp", "5.39", "31 Dec 2025")
board("Andi Mallarangeng", "co_tspc", "Independent Commissioner", "C")
board("Idrus Marham", "co_mknt", "Commissioner", "C", "low", NM + "; not confirmed against a second source")
board("Rahayu Saraswati", "co_vici", "Vice President Commissioner", "C")
stake("Rahayu Saraswati", "co_trin", "3.92", "30 Jun 2026")
board("Condro Kirono", "co_nest", "Independent Commissioner and Chairman of the Audit Committee", "C")
board("Budi S. Tanuwibowo", "co_ahap", "Independent Commissioner", "C")
add("Hashim Djojohadikusumo", "co_arsari", "Founder and Chairman", "H", "founder", sid="S046")
add("Luhut Binsar Pandjaitan", "co_toba_sejahtra", "Owner", "N", "owner", src="news", sid="S047", conf="medium",
    note="Press reports attribute the Toba Sejahtra stake in TBS Energi Utama to him; the company register was not consulted")
add("Erick Thohir", "co_beyond_media", "Owner", "N", "owner", src="news", sid="S049", conf="medium",
    note="Described as owner of the parent entity of Mahaka Media; the company register was not consulted")
add("Erick Thohir", "co_abba", "President Commissioner", "C", "founder", end="2019-12", status="past", src="news", sid="S048",
    note="Founder of the Mahaka group; resigned on joining the cabinet")
add("Erick Thohir", "co_mari", "President Commissioner", "C", "appointed", end="2019-12", status="past", src="news", sid="S048",
    note="Resigned on joining the cabinet")
add("Kaesang Pangarep", "co_hbk", "Owner", "N", "owner", src="news", sid="S050", conf="medium",
    note="PMMP stated on 10 July 2026 that Harapan Bangsa Kita is a minority shareholder bought on the market")

write("sources.csv", S)
write("organizations.csv", O)
write("memberships.csv", M)
print(f"sources {len(S)}, organizations {len(O)}, memberships {len(M)}")

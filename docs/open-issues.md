# Open issues, version 0.2.0

## Decisions for the maintainer

- **Licence.** CC BY 4.0 was chosen on 12 November 2026 and covers data, documentation and scripts. A software licence such as MIT could be added for the scripts alone if code reuse matters.
- **Visibility.** A private repository is advisable at first because `ties.csv` names family relationships and `persons.csv` names spouses.
- **Published scope.** All 208 people are in the tables. The 142 core people are the rows with `snapshot_layer` of `current` or `security`.

## Conflicts found while building 0.1

- **Raja Juli Antoni.** The snapshot file seats him on the PSI board on 12 November 2026. Suara.com reports that he resigned as secretary general and gave up all party activity on 9 November 2026. The snapshot row is kept and marked as ended. `partisan_status` still reads `party`; decide whether he should now be `non_party`. The same report says Giring Ganesha and Isyana Bagoes Oka left with him, and neither is in the dataset.
- **Joko Widodo.** The snapshot file codes him as non-party. Wikidata lists PDIP for 2004 to 2024 and PSI from 2025. Both rows are stored with `src = wikidata`; the PSI row needs a party source or removal.
- **Party not coded in the snapshot file but named by Wikidata** for 25 further people, among them Luhut Binsar Pandjaitan (Golkar), Khofifah Indar Parawansa, Mahfud MD and Saifullah Yusuf (PKB), Dody Hanggodo and Soekarwo (Demokrat), Sakti Wahyu Trenggono (PAN). These rows have `status_asof = unknown`. Each needs a decision on current status.
- **Kemendagri Pelita dataset 888** turned out to be a register of party chairs and secretaries general from before mid 2023, not regional heads. Governors are now coded from another source (see below).
- **Gelora.** The Kemendagri register gives Fahri Hamzah as secretary general, while the dataset codes Mahfudz Siddiq in that post from 2019 from background knowledge. One of the two needs a document.
- **Birth dates.** The KPU filing and Wikidata disagree for Bambang Wuryanto (KPU 1956-07-17, Wikidata 1958-07-17), Deddy Sitorus (1970-11-17 against 1970-01-17) and Viva Yoga Mauladi (1968-06-30 against 1968-05-30). The KPU dates are stored because the candidates filed them.
- **Garuda.** The dataset held Partai Garuda twice, under its Wikidata name and its ballot name. The two are now one organisation, `party_garuda`.
- **Party chairs missing from the dataset.** The register names chairs who are not among the 208 people: Muhamad Mardiono (PPP), Hary Tanoesoedibjo (Perindo), Oesman Sapta Odang (Hanura), I Gede Pasek Suardika (PKN), Ridho Rahmadi (Ummat) and Muzakir Manaf (Partai Aceh). Decide whether the scope should cover every party that can join a nominating coalition.

## Governors, version 0.2.0

- **Inauguration dates** now rest on inauguration reports: 33 governors on 20 February 2025, Aceh on 12 February, Bangka Belitung and Papua Pegunungan on 17 April, Papua on 8 October 2025. The date of SF Hariyanto's appointment as acting governor of Riau (5 November 2025) still comes from Wikipedia; the press report confirms the appointment without a date.
- **Birth dates** were checked against Kompaspedia and the ICW candidate profiles. Three sources disagree in these cases:
  - Yulius Selvanus: Kompaspedia gives 16 September 1963 in Tana Toraja, ICW and Wikipedia give 17 September 1963 in Semarang. The month is stored.
  - Apolo Safanpo: Kompaspedia gives 25 April 1975, ICW (citing detik.com) and the provincial website give 24 April. The 24th is stored.
  - Sherly Tjoanda: Kompaspedia gives 8 August 1982, Wikipedia 12 August; ICW notes that sources differ on the year. 8 August 1982 is stored.
  - Zainal Arifin Paliwang: Kompaspedia gives 16 December 1962, English Wikipedia 6 December. The 16th is stored.
  - Dedi Mulyadi: his KPU filing gives 12 April 1971 (stored), Kompaspedia 11 April.
  - John Tabo and Mathius D. Fakhiri rest on one compiled source each (ICW).
- **Party rows** were recoded for the 35 people added as governors. Rows with `src = wikipedia` (13 of 43, for 11 people) found no better source and need a party or press document: Al Haris, Helmi Hasan, Lalu Muhamad Iqbal, Ria Norsan (Gerindra), Agustiar Sabran (Gerindra), Muhidin, Mathius D. Fakhiri, Apolo Safanpo, Meki Fritz Nawipa, Elisa Kambu (Gerindra) and Muzakir Manaf (Partai Aceh).
  - Sherly Tjoanda has no party row. Wikidata lists Demokrat and Wikipedia lists her as independent; she replaced her late husband as the candidate of an eight party coalition.
  - Andi Sudirman Sulaiman: Kompaspedia tags him with Gerindra, Wikipedia lists him as independent. Stored with low confidence and unknown status.
  - Muzakir Manaf appears as adviser to Gerindra's Aceh board on the party's own list, which is undated; Wikipedia ends his Gerindra affiliation in 2022.
  - Regional party posts older than 2025 (Herman Deru, Rudy Mas'ud, Hidayat Arsani) are kept in the note and not as the role.
- The ICW profile of Yulius Selvanus reports, citing the KPU, that he declared a legal history as a member of Tim Mawar. `legal_status` is coded only from the DPR candidate filings of 2024, so this is not coded.
- Leads from the same sources, not coded because the relatives are not in the dataset: Agustiar Sabran is the elder brother of former governor Sugianto Sabran; Rudy Mas'ud's brothers hold or held office in Balikpapan, the East Kalimantan DPRD and Penajam Paser Utara; Zainal Arifin Paliwang's wife sits in the DPR.
- Security backgrounds for Ahmad Luthfi, Mathius D. Fakhiri, Zainal Arifin Paliwang, Andi Sumangerukka and Yulius Selvanus rest on their Wikipedia biographies; Kompaspedia and ICW confirm the academy classes of Fakhiri (Akpol 1990) and Sumangerukka (Akmil 1987).
- Riau has a suspended governor, Abdul Wahid, and an acting governor, SF Hariyanto. If the conviction becomes final and a governor is appointed, both rows need end dates.

## Organisation boards and companies, version 0.2.0

- Posts were coded for 59 people, 35 of them among the 142 core people. Boards read in full were PBNU 2026 to 2031, MUI 2025 to 2030, PP Muhammadiyah 2022 to 2027 and the KADIN leadership. The PBNU list of 2022 to 2027 was read without its Tanfidziyah section, so posts such as vice chair and chair held in that term are missing.
- The report on the Masyarakat Ekonomi Syariah board names a selection of each council, and the KADIN site shows the chairs of its councils without their members.
- Boards not found in a readable form were PB IKA PMII, the KAHMI councils, ICMI (a congress was under way in November 2026), Pemuda Pancasila after its congress of October 2026, ISNU, Pepabri, MATAKIN and Permabudhi. Their existing rows keep `src = mem`.
- Five rows identify a person by name alone in a board list: Irfan Yusuf, Herman Deru and Agustiar Sabran in PBNU, and Rudy Mas'ud in MUI, where the list spells the name Rudi Mas'ud. They carry `confidence = medium`.
- Posts taken from Wikipedia (DMI, PGI, PA GMNI, KSPSI, PSSI, KNPI and HKTI before 2015) should be replaced with the organisations' own records.
- Company rows rest on a name match against the management and shareholder lists of the 964 listed companies. Idrus Marham as commissioner of Mitra Komunikasi Nusantara is the least certain and carries `confidence = low`. Ignasius Jonan appears at United Tractors as chair of the audit committee and is absent from its list of commissioners.
- Ownership through holding companies is coded for three people on the strength of press reports (Luhut Binsar Pandjaitan and Toba Sejahtra, Erick Thohir and Beyond Media, Kaesang Pangarep and Harapan Bangsa Kita). The stakes of Mega Corpora in Bank Mega and of the Mayapada companies in Bank Mayapada are written in the organisation notes, with no ownership row for Chairul Tanjung or Tahir, because no source read for this version names the ultimate owner.
- Private groups are almost absent. Only Arsari Group is coded, from its own website. Groups such as CT Corp, Lion Air, Bosowa, Media Group, Tiran, Recapital and the Gobel companies need the company register or annual reports.
- Company and organisation rows have no start dates where the list gives none.
- The KPU list behind the DPR results shows who was declared elected. Winners who then took another office, such as Dedi Mulyadi, still read `won`.

## Ethnicity

- `ethnicity` is coded for 135 of 243 people (78 of the 142 core people) from the ethnic categories on their Wikipedia articles. A category is an editor's label, often placed without a citation, so each value needs a biography, an interview or a profile before it is used in analysis.
- Fifteen people carry more than one group. Some combinations look doubtful and were kept as found: Anies Baswedan (Arab Indonesian and Sundanese), Chairul Tanjung (Minangkabau and Sundanese, English edition only), Grace Natalie (Chinese Indonesian and Malay), Ma'ruf Amin (Arab Indonesian, Javanese and Sundanese).
- The Indonesian edition was read for all 243 names and the English edition for about 100 people who had no ethnic category there. The filter held 50 category names per edition, so a person filed only under a narrower category, such as a category for Javanese clerics or Minangkabau soldiers, was missed.
- Province and city categories were set aside, which leaves empty some people whom the Indonesian edition files only under Tokoh Aceh (Surya Paloh, Teuku Riefky Harsya, Muzakir Manaf), Tokoh Lampung, Tokoh Banten, Tokoh Maluku, Tokoh Gorontalo or Tokoh Papua.
- About 25 people have no article under the name used here, and three names led to a different person (Mohamad Hatta, Sugiono, Abdul Wahid); none of these is coded.
- Wikidata's ethnic group property (P172) was not read because the query service did not respond through the browser.

## Verification queue

- 128 membership rows carry `src = mem`. They are the 94 rows inherited from the snapshot file and 34 added since (past offices, party posts and 20 posts in mass organisations and business associations that no published board confirmed). A further 17 roles on snapshot rows (8 others are now confirmed by the register), 23 academy classes and the 21 presidential candidacy rows also rest on background knowledge. Official KPU results should replace the presidential rows first, since they are the easiest to document.
- 247 of the 288 snapshot rows have no role. The cabinet list of 1 October 2026 would supply the ministry and title for the 74 `reg` rows, and should replace the cluster bodies with the actual ministries.
- 28 people have no Wikidata match: Arief Anshory Yusuf, Arief Rosyid Hasan, Ariyo Windutomo, Budi Santoso, Chatib Basri, Dominggus Oktavianus, Fauzan, Firman Hidayat, Haris Rusly Moti, Hasanuddin Wahid, Heriyanto Irawan, Iftitah Sulaiman, Irwan Fecho, Jeffrie Geovanie, Jumhur Hidayat, Jusuf Hamka, Maman Abdurrahman, Mohamad Hatta, Muhammad Kholid, Muhammad Qodari, Noerhadi, Philip K. Wijaya, Rachmat Gobel, Septian Hario Seto, Sudaryono, Sylvester Matutina, Utje Gustaaf Patty, Wishnu Wardhana. Several have items under other spellings. Matches that returned a namesake (a badminton player for Budi Santoso, a footballer for Maman Abdurrahman, a cyclist for Firman Hidayat) were discarded, and so was the Wikidata party statement for Pandu Sjahrir, which appears to belong to his father.
- Wikidata birth dates and places are stored as retrieved and have not been compared with KPU or official profiles. Hashim Djojohadikusumo's date was left empty because the Wikidata value looked like a placeholder.
- The PBNU leadership was in dispute in late 2025. The rows for Yahya Cholil Staquf as chair and Saifullah Yusuf as secretary general now end in 2026, the year of the next board, and either post may have ended earlier.

## Leads not coded

The KPU file lists DPR candidates of 2024 who share a name with people in the dataset, among them Hisan Anis Matta, Siti Mamduhah Ma'ruf Amin, Prananda Surya Paloh, Putri Zulkifli Hasan and Rio Dondokambey. A shared name is not evidence of kinship, so no tie was coded; each needs a public record before it enters `ties.csv`.

Two spouses named in the KPU filings hold public office themselves: Netty Prasetiyani, filed as the spouse of Ahmad Heryawan, and Ratu Rachmatu Zakiyah, filed as the spouse of Yandri Susanto. Adding them as people would turn both marriages into coded ties.

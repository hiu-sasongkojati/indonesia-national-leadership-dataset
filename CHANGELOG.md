# Changelog

## 0.2.0, 13 November 2026

- Restructured the data into `persons`, `organizations`, `memberships` and `ties`, and kept the three original files in `data/snapshot/` with checksums.
- Matched 68 people to their KPU filings for the DPR election of 2024 (Kuipers' file) and added those candidacies with constituency, party and list number, then coded the result and vote count of each from the KPU list of elected candidates.
- Added the Kemendagri register of party boards. Thirteen existing posts now cite it, and seven earlier posts were added (Ahmad Muzani, Ahmad Syaikhu, Teuku Riefky Harsya, Eddy Soeparno, Yusril Ihza Mahendra, Afriansyah Noor, Yohanna Murtika).
- Added academy classes and security backgrounds for the five governors who are retired police or army generals.
- Coded posts in religious, student and business organisations from published boards: PBNU 2026 to 2031 and 2022 to 2027, MUI 2025 to 2030, PP Muhammadiyah, KADIN, KAHMI, Masyarakat Ekonomi Syariah, Muslimat NU, HKTI, DMI, PGI and others.
- Added the `company` domain with 25 companies and 29 rows of board seats and shareholdings, found by matching every person against the management and shareholder lists of the 964 listed companies. Two listed state enterprises were added to `state_enterprise`.
- New vocabulary: `role_level = regional_board`, `basis = owner` and `src = idnfinancials`. The wide table gains `no_current_seat` in place of `no_coded_seat`, and the columns `company_board` and `company_ownership`.

## 0.1.0, August 2025

- Established the first version of the relational dataset.
- Typed every organisation by domain and added parties, mass organisations, business associations and provincial governments.
- Added kinship ties linking Bobby Nasution to Joko Widodo and Kaesang Pangarep, Andi Sudirman Sulaiman to Amran Sulaiman, and Zulkifli Hasan to Helmi Hasan.
- Added `education` (academy classes) and `candidacies` (presidential tickets 2004 to 2024).
- Added `ethnicity` and `ethnicity_src` to `persons`, coded for 135 people from the ethnic categories on their Wikipedia articles.
- Coded the sitting governor of every one of the 38 provinces and limited regional executives to the provincial level. Thirty-five people were added, among them the suspended governor of Riau alongside the acting governor. Party rows, inauguration dates and birth dates come from Kompaspedia, the ICW candidate profiles, the Gerindra list of provincial boards, Sekretariat Kabinet releases and press reports, in place of Wikidata.
- Added marital status, spouse name, number of children and declared legal status from the KPU filings of 2024 for the 42 matched people whose profiles were open. Spouse names are published as filed.

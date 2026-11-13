# Indonesia National Leadership Dataset

A relational dataset of Indonesian national elites, their institutional affiliations across state bodies, political parties, mass organisations, business associations and publicly listed companies, and documented interpersonal ties. Constructed to analyze potential challengers and nominating coalitions ahead of the 2029 presidential election.

Coverage (as of 13 November 2026): 243 individuals and 30 documented interpersonal ties (kinship, principal–aide, and career linkages). National state bodies, governors of all 38 provinces, political party executive boards, mass and business organizations, and listed corporate boards. Every affiliation record is time-stamped, sourced, and sorted by institutional domain.

Note: Data processing and network construction scripts in Python were originally developed with scripting assistance from Claude Sonnet 5.5.

## Layout

```
data/
  persons.csv  organizations.csv  memberships.csv  ties.csv
  education.csv  candidacies.csv  sources.csv
  snapshot/            the snapshot of 12 November 2026 in its original three-file form, with checksums
derived/
  persons_wide.csv           one row per person, one column per affiliation domain
  memberships_labeled.csv    memberships with names in place of identifiers
docs/
  codebook.md  open-issues.md
scripts/
  build_from_snapshot.py  make_wide.py  validate.py  seeds/
```

## What each table holds

| Table | Rows | Contents |
| --- | --- | --- |
| `persons` | 243 | identifier, gender, birth date and place (Wikidata and KPU, about 80 per cent filled), religion, ethnicity as categorised on Wikipedia (56 per cent), minimum degree, marital status, spouse, number of children and declared legal status from the KPU filing of 2024 (about 20 per cent), partisan status, security background |
| `organizations` | 156 | 33 snapshot bodies, 26 parties, 26 mass organisations, 2 business associations, 38 provincial governments, 25 companies, 2 listed state enterprises and 4 parent or past bodies, each with a domain and type |
| `memberships` | 576 | the 288 seats of the snapshot of 12 November 2026 plus 288 rows: the sitting governor of every province, party history, party posts, mass organisation and business association posts, company board seats and shareholdings, and past cabinet posts |
| `ties` | 30 | kinship, aide and cohort ties |
| `education` | 27 | military and police academy classes |
| `candidacies` | 89 | presidential and vice presidential tickets 2004 to 2024, and 68 DPR candidacies of 2024 from the KPU filings with the result and vote count |

In `derived/persons_wide.csv` the former affiliation field becomes separate columns: `religion`, `ethnicity`, `highest_degree`, `marital_status`, `spouse_name`, `n_children`, `legal_status`, `dpr_candidacy_2024`, `party_current`, `party_role_current`, `party_other`, `executive_current`, `legislature_current`, `security_current`, `advisory_current`, `state_enterprise_current`, `regional_current`, `offices_past`, `campaign_2024`, `ormas_religious`, `ormas_student_youth`, `ormas_other`, `business_assoc`, `company_board`, `company_ownership`, `academy_cohort`, `kin_ties`, `aide_ties`, `cohort_ties` and `presidential_candidacies`.

## Use

```
python3 scripts/validate.py      # integrity checks and proof that the snapshot is recoverable
python3 scripts/make_wide.py     # rebuild derived/ after editing data/
```

Python 3.8 or later, standard library only. `scripts/import_kpu_kemendagri.py` records how version 0.2 was built; rerunning it, or `scripts/import_kpu_family_legal.py`, needs Kuipers' file `candidate_pileg_data_2024.csv`, downloaded from https://nicholaskuipers.com/data and placed in `data/external/raw/`, where git ignores it. `scripts/build_from_snapshot.py` documents how version 0.1 was derived from `data/snapshot/` and `scripts/seeds/`; from here on the tables in `data/` are edited directly.

The snapshot of 12 November 2026 is the set of membership rows with `in_snapshot = 1`, and `validate.py` rebuilds its three files from the tables and compares them field by field.

## Reliability

Every membership record includes a source code. `reg`, `news` and `official` rest on a document, and `kemendagri` and `kpu2024` on government records. `idnfinancials` rows originate from a financial data aggregator republishing Indonesia Stock Exchange (IDX) disclosures; most of them identify the person by name alone without secondary biographical identifiers. `mem`, `snapshot` and `wikidata` lack primary documented verification, with 128 rows retaining `mem`. Read `docs/open-issues.md` before using the organisation and company rows in analysis.

## Design

The relational schema follows the Popolo open civic data specification (modeling persons, organizations, and memberships). Individual background attributes draw on the Paths to Power dataset and the LPEM-FEB UI study of Indonesian local leaders, while institutional domain classifications follow Marcus Mietzner's framework of the coalition actors Indonesian presidents incorporate into governing alliances. Complete column definitions are documented in `docs/codebook.md`.

## Data sources and attribution

This dataset builds on work by others. Please credit them as well as this repository when you use the fields that come from them.

- **Indonesian Legislative Candidate Profiles, 2024**, compiled by Nicholas Kuipers (Princeton University) from the candidate pages of the Komisi Pemilihan Umum (KPU) in February 2024 and published at https://nicholaskuipers.com/data. The DPR candidacies of 2024 in `data/candidacies.csv` and the `religion`, `highest_degree`, `marital_status`, `spouse_name`, `n_children`, `legal_status` and some `birth_date` values in `data/persons.csv` come from this file. It is not redistributed here.
- **Data pengurus partai politik**, Kementerian Dalam Negeri, Pelita dataset 888 (https://pelita.kemendagri.go.id/kemendagri/dataset/888/tabel-data), downloaded on 12 November 2026 and kept unchanged in `data/external/kemendagri/` (source `kemendagri`).
- **Kompaspedia** profiles (Kompas), the **Kamu Bersih Aku Pilih** candidate profiles of Indonesia Corruption Watch (https://kamubersihakupilih.id), the Gerindra list of provincial boards, Sekretariat Kabinet releases and press reports, for the governors' birth dates, inauguration dates and party rows. Each row cites its source in `data/sources.csv`.
- **Organisation boards** published by NU Online, Muhammadiyah and KADIN Indonesia, and press reports of the boards of MUI, KAHMI, Masyarakat Ekonomi Syariah, Muslimat NU, HKTI, HIPMI and IMI, for posts in religious, student and business organisations.
- **IDNFinancials** (https://www.idnfinancials.com), for the management and shareholder lists of the 964 companies on the Indonesia Stock Exchange, read on 13 November 2026 (source `idnfinancials`).
- **Komisi Pemilihan Umum**, for the list of candidates declared elected to the DPR in 2024, as published by KPU Papua Pegunungan.
- **Wikipedia**, Indonesian and English editions, for the ethnic categories attached to each person's article (`ethnicity`), read on 13 November 2026.
- **Wikidata** (https://www.wikidata.org), CC0 1.0, for gender, birth dates, birthplaces and some party histories (source `wikidata`).

## Licence and citation

The repository is licensed under CC BY 4.0 (see `LICENSE`). See `CITATION.cff` for how to cite the dataset.

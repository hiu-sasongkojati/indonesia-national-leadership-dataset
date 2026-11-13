# Codebook, version 0.2.0

Snapshot date 12 November 2026. All files are UTF-8 CSV with every field quoted. Dates are written `YYYY`, `YYYY-MM` or `YYYY-MM-DD` according to how precisely the source gives them. An empty field means "not coded", never "no".

## How the tables fit together

`persons` and `organizations` are registers. `memberships` joins them, one row for each spell that one person spends in one body. `ties` holds relationships between two people that no shared body captures. The remaining tables hang off `person_id`. The files in `derived/` are rebuilt from these tables by `scripts/make_wide.py` and are never edited by hand.

| File | Rows | One row is |
| --- | --- | --- |
| `data/persons.csv` | 243 | one person |
| `data/organizations.csv` | 156 | one organisation or one body inside it |
| `data/memberships.csv` | 576 | one person in one body for one spell |
| `data/ties.csv` | 30 | one documented tie between two people |
| `data/education.csv` | 27 | one qualification of one person |
| `data/candidacies.csv` | 89 | one person on one ticket in one round, or on one party list for one constituency |
| `data/sources.csv` | 52 | one source |
| `data/external/kemendagri/` | 24 | the Kemendagri register of party chairs and secretaries general, as downloaded |
| `data/snapshot/*.csv` | 208, 288, 26 | the snapshot of 12 November 2026 in its original three-file form |

## persons.csv

| Column | Meaning | Values |
| --- | --- | --- |
| `person_id` | stable identifier, `P0001` to `P0208` in the alphabetical order of the snapshot file; new people take the next number | |
| `name` | the spelling used in the snapshot files, unique | |
| `gender` | | `M`, `F` |
| `birth_date`, `birth_place` | birth date from the KPU filing where the candidate opened the profile, otherwise Wikidata (a Wikidata date of 1 January is stored as the year alone); birth place from Wikidata only, because the KPU column of that name records the district of residence | |
| `partisan_status` | whether the snapshot file named a party | `party`, `non_party`, `not_coded` |
| `party_snapshot` | the party label in the snapshot `nodes.csv` | |
| `security_service`, `security_status`, `security_rank_band` | the snapshot `security_bg` split into three fields | `TNI`, `Polri`; `active`, `retired`, `former`; `flag`, `junior` |
| `wikidata_qid` | Wikidata item, 180 of 208 matched | |
| `bio_src` | sources of the birth date (and of gender and birth place where no other source is named), separated by semicolons | `wikidata`, `kpu2024`, `kompaspedia` (S017), `icw` (S018) |
| `religion` | coded only from the person's own declaration in the KPU candidate filing of 2024; empty where the person did not stand or closed the profile | `Islam`, `Protestant`, `Catholic`, `Hindu`, `Buddhist`, `Confucian` |
| `ethnicity` | ethnic group or groups under which Wikipedia editors categorise the person's article, several separated by `; `. A category that names a province or a city (Tokoh Lampung, Tokoh Bali, Tokoh Aceh and the like) is not used, because it marks where a person comes from. Empty where the article has no ethnic category or no article was found | `Javanese`, `Sundanese`, `Minangkabau`, `Batak`, `Bugis`, `Madurese`, `Malay`, `Banjarese`, `Betawi`, `Balinese`, `Acehnese`, `Minahasan`, `Torajan`, `Mandarese`, `Dayak`, `Sasak`, `Nias`, `Lampung`, `Papuan`, `Indo`, `Chinese Indonesian`, `Arab Indonesian`, `Indian Indonesian` |
| `ethnicity_src` | Wikipedia edition that carries the category (S051, S052) | `idwiki`, `enwiki`, `idwiki+enwiki` |
| `highest_degree` | highest credential held | `secondary`, `diploma`, `S1`, `S2`, `S3`, `academy` |
| `highest_degree_src` | how `highest_degree` was coded. In 0.2 every value is the lowest degree proved by the academic titles on the 2024 ballot name (Dr. or Ph.D. gives S3; M.Si., M.A. and similar give S2; S.H., S.E., Ir., Drs. and similar give S1; A.Md. gives diploma). Honorary doctorates and "Prof." alone are not counted, and a ballot without titles leaves the field empty | |
| `degree_field` | field of that credential, sixteen categories of Paths to Power | not coded in 0.1 |
| `studied_abroad` | at least one year of study abroad | `0`, `1`; not coded in 0.1 |
| `marital_status` | as filed with the KPU in February 2024 | `married`, `unmarried` |
| `spouse_name` | spouse as filed with the KPU, spelled as filed; empty where the candidate gave a placeholder or withheld it | free text |
| `n_children` | number of children as filed with the KPU | whole number |
| `legal_status` | the criminal record status the candidate declared to the KPU | `none_declared` (Tidak Memiliki Status Hukum), `former_convict` (Mantan Terpidana), `former_convict_on_parole`, `former_convict_culpa`, `convicted` |
| `family_legal_src` | source of the four fields above | `kpu2024` |
| `pre_political_occupation` | main work in the decade before full time politics | `military`, `police`, `civil_servant`, `business`, `professional`, `academic`, `religious_leader`, `activist`, `media`, `legislator_staff`, `other`; not coded in 0.1 |
| `political_family` | a parent or grandparent held political office | `0`, `1`; not coded in 0.1 |

## organizations.csv

| Column | Meaning |
| --- | --- |
| `org_id` | identifier with a prefix for the domain, for example `party_golkar`, `ormas_nu`, `exec_dpn` |
| `name`, `name_long` | short label and full name |
| `domain` | the kind of political resource the body represents (see below) |
| `org_type` | finer type inside the domain |
| `parent_org_id` | the organisation a body belongs to, for example `party_golkar_dpp` → `party_golkar`, `ormas_nu_ansor` → `ormas_nu` |
| `stream` | religious or ideological stream where the literature assigns one |
| `snapshot_name` | exact string used in the snapshot `affiliations.csv`, for the 33 snapshot bodies |

| `domain` | `org_type` values in use | Column in the wide table |
| --- | --- | --- |
| `party` | `party`, `party_central_board` | `party_current`, `party_role_current`, `party_other` |
| `executive` | `cabinet_cluster`, `presidential_office`, `state_council`, `past_cabinet` | `executive_current`, `offices_past` |
| `legislature` | `chamber_leadership` | `legislature_current` |
| `judiciary` | `constitutional_court` | `offices_past` |
| `security` | `armed_forces_leadership`, `police_leadership`, `intelligence_leadership`, `defence_ministry_leadership` | `security_current` |
| `advisory` | `presidential_advisory_council`, `economic_council`, `special_adviser` | `advisory_current` |
| `state_enterprise` | `sovereign_fund`, `sovereign_fund_board`, `listed_state_enterprise` | `state_enterprise_current` |
| `regional_government` | `province` (all 38 provinces) | `regional_current`, `offices_past` |
| `campaign` | `presidential_campaign_team` | `campaign_2024` |
| `mass_organization` | `religious`, `religious_council`, `religious_institution`, `religious_youth_wing`, `religious_women_wing`, `religious_professional_wing`, `religious_economic_society` | `ormas_religious` |
| `mass_organization` | `student`, `student_alumni`, `youth` | `ormas_student_youth` |
| `mass_organization` | `labour`, `veterans`, `sports`, `farmers_association` | `ormas_other` |
| `business_association` | `chamber_of_commerce`, `young_entrepreneurs` | `business_assoc` |
| `company` | `listed_company`, `holding_company`, `private_group` | `company_board`, `company_ownership` |

Domains to add when coding reaches them: `think_tank`, `university` (rectorates and alumni associations such as ILUNI or KAGAMA), `volunteer_network` (relawan groups).

## memberships.csv

| Column | Meaning | Values |
| --- | --- | --- |
| `membership_id` | `M0001` onward; `M0001` to `M0288` are the snapshot rows in their original order | |
| `person_id`, `org_id` | keys | |
| `role` | title as used by the body, in Indonesian | free text |
| `role_level` | seniority of the role | `head` (ketua umum, presiden partai, rais aam, gubernur), `deputy_head`, `regional_board` (chair or adviser of a party's provincial board, such as Ketua DPD or Ketua DPW), `executive_board` (sekjen, bendahara, ketua, wakil ketua umum, minister), `council` (dewan pembina, majelis tinggi, majelis syura, mustasyar, a company's board of commissioners), `member`, `not_coded` |
| `basis` | how the person belongs | `ex_officio`, `roster` (named on a published list of the body), `elected`, `appointed`, `founder`, `cadre_or_member`, `party_affiliation` (party named without a post), `alumni`, `cultural_affiliation`, `owner` (shareholder or owner of a company) |
| `start_date`, `end_date` | bounds of the spell | |
| `status_asof` | state on the snapshot date | `current`, `past`, `unknown` |
| `snapshot_layer` | the snapshot `layer` | `current`, `security`, `advisory`, `historical`, `prabowo`, empty |
| `in_snapshot` | `1` for the 288 rows of the snapshot file | `0`, `1` |
| `src`, `source_id` | source of the row | the codes in the table below |
| `role_src`, `role_source_id` | source of the role and dates where they were added after the snapshot | same codes |
| `confidence` | coder's confidence in rows added in 0.1 | `high`, `medium`, `low` |
| `note` | | |

### Source codes

| `src` | Meaning | Standing |
| --- | --- | --- |
| `reg` | ex officio seat read from the cabinet list of 1 October 2026 or the founding regulation | documentary |
| `news` | named in a press report retrieved on or before 12 November 2026 | press |
| `mem` | written from background knowledge to mid 2026 and not checked against a document | unverified |
| `snapshot` | carried from a snapshot column that had no source code (the party column, lineage ties) | unverified |
| `wikidata` | Wikidata statement retrieved on 12 November 2026 | unverified secondary |
| `kemendagri` | Kemendagri register of party boards (S005); confirms that the post was held at the time of the register, before mid 2023, and says nothing about the date it ended | documentary, dated |
| `kpu2024` | the person's own KPU candidate filing for the DPR election of 2024 (S006) | documentary |
| `wikipedia` | Wikipedia list of sitting governors (S009) or biography (S011, S027), retrieved on 13 November 2026; used only where no better source was found | secondary |
| `official` | publication of a government body, a party, an organisation or a company about itself (Sekretariat Kabinet releases, the Gerindra list of provincial boards, the PBNU, Muhammadiyah and KADIN boards) | documentary |
| `profile` | profile compiled by a research desk from primary sources: Kompaspedia (S017) and the ICW candidate profiles (S018) | secondary, curated |
| `idnfinancials` | management or shareholder list of a listed company as shown by IDNFinancials on 13 November 2026 (S045), which republishes filings to the stock exchange | secondary, from filings |

A row should move from `mem`, `snapshot` or `wikidata` to `reg` or `news` as soon as a document supports it, with the document added to `sources.csv`.

### Regional executives

Executive leadership below the national level is coded for the 38 provinces only. Each province has one current row for the person who heads it: the elected governor (`role_level = head`, `basis = elected`), or, where the elected governor is suspended, the acting governor (`basis = appointed`) next to a current row for the suspended governor whose role ends in "(nonaktif)". The Sultan of Yogyakarta holds the governorship by virtue of the throne. Vice governors, regents and mayors are out of scope. The start date is the inauguration for the current term. A governor's party is coded as membership of the party (`cadre_or_member`), with a provincial party post as the role where a current source names one; the coalition that nominated the governor in 2024 is not coded.

### Companies

The `company` domain holds listed companies, holding companies and private groups. Listed state enterprises stay in `state_enterprise`. A president director is coded `head`, a director `executive_board` and every commissioner `council`, with the full title kept in `role`. A shareholding is a row with `basis = owner` and `role_level = not_coded`; the role gives the percentage and the reporting date for a direct holding, and reads `Owner` where the press attributes a holding company to the person. Stakes held by one company in another are written in the `note` of the organisation. Board and shareholder rows were found by matching the 243 names against the lists of all listed companies, so a seat held under a different spelling, or a stake held through a nominee, is absent. No start dates are recorded because the lists give none.

### Coding rules

1. **One spell, one row.** A person who leaves a post and returns gets two rows. A change of role inside the same body also starts a new row.
2. **Bodies inside parties.** A seat on a central board is coded against the board (`party_x_dpp`), whose parent is the party. Membership without a post is coded against the party itself.
3. **Mass organisations.** Code a post where there is one. Code `cadre_or_member` when a source names formal membership or cadre training. Use `cultural_affiliation` for a publicly stated identification without membership, such as schooling in the organisation's institutions; a family background alone is not coded as membership.
4. **Dates.** Give the precision the source gives. Leave a bound empty when unknown and set `status_asof` to `unknown` when neither the end date nor current standing is documented.
5. **Snapshot.** The snapshot of 12 November 2026 is the set of rows with `in_snapshot = 1`. A snapshot row found to have ended before that date keeps the flag and gains an `end_date` (see Raja Juli Antoni, `party_psi_dpp`).
6. **New people.** Add the person to `persons.csv` first, then at least one membership or candidacy with a source.

## ties.csv

`tie_id`, `person_a_id`, `person_b_id`, `tie_type` (`kinship`, `aide`, `cohort`), `note` (the relationship in words, with years where known), `spec` (`prabowo` for the eight ties to Prabowo Subianto, `main` for the rest), `start_date`, `end_date`, `src`, `source_id`. Person A is the senior party in `aide` ties and the older generation in `kinship` ties where there is one. Cohort ties can now be derived from `education.csv` and need hand coding only where a source stresses the bond.

## education.csv

`education_id`, `person_id`, `institution`, `institution_type` (`military_academy`, `police_academy`, `police_officer_school`, `university`, `pesantren`, `school`), `level`, `field`, `grad_year`, `country`, `src`, `source_id`, `confidence`, `note`. Version 0.1 holds academy classes for 24 officers and former officers.

## candidacies.csv

`candidacy_id`, `person_id`, `election_type` (`presidential`, `legislative`), `election_year`, `round`, `position` (`president`, `vice_president`, `DPR`), `running_mate`, `vote_share_pct` (share of the ticket), `outcome` (`won`, `lost`, `advanced`), `votes` (personal vote of a winning DPR candidate), `outcome_source_id`, `constituency` (KPU electoral district), `party_org_id` (nominating party), `list_number`, `declared_occupation` (KPU category, for example `ANGGOTA DPR`), `profile_open` (`1` when the candidate published the full profile), `src`, `source_id`, `confidence`, `note`.

The 68 legislative rows were matched by hand on name, party and constituency, with birth date as a check where the profile was open. Namesakes standing for regional councils were discarded. Address and campaign statements in the KPU file were not imported. A DPR candidate named on the KPU list of the 580 declared elected (S029) is coded `won` with the vote count shown there, and a candidate absent from it is coded `lost`. The list records who was declared elected. It does not show who was sworn in or who has since left the seat for another office.

## derived/persons_wide.csv

One row per person and 42 columns. `no_current_seat` is 1 for people with no current post in any coded body, party membership without a post aside. The table includes `religion`, `ethnicity`, `highest_degree`, the four fields from the KPU filing on family and legal status, and `dpr_candidacy_2024`. `company_board` lists seats on company boards and `company_ownership` lists shareholdings. Each affiliation domain has its own column, filled with the names of the bodies and, where coded, the role and dates. `party_current` uses rows with `status_asof = current`; `party_other` lists every other party on record with its dates and status. `security_bg` reproduces the snapshot string. `n_snapshot_seats`, `n_core_seats` and `no_coded_seat` are counts over the snapshot rows.

## Sensitive attributes

The dataset covers people in national public roles. Religion, marital status, spouse, number of children and legal status are taken only from what candidates filed publicly with the KPU in 2024, and spouse names are published even where the spouse holds no public role. Ethnicity is recorded only as Wikipedia categorises the person, with the edition named in `ethnicity_src`. Health, private wealth and home addresses are not coded. Kinship ties in `ties.csv` name relatives who are themselves in the dataset and cite a public record; a spouse named in `persons.csv` enters `ties.csv` only once the spouse is added as a person.

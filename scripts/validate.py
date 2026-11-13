#!/usr/bin/env python3
"""Check the tables in data/ and prove that the snapshot is still recoverable.

Run from the repository root:  python3 scripts/validate.py     (exit status 1 on any failure)
"""
import csv, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D, SNAP = ROOT / "data", ROOT / "data" / "snapshot"
fails = []


def read(p):
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def check(ok, msg):
    print(("ok    " if ok else "FAIL  ") + msg)
    if not ok:
        fails.append(msg)


P, O, M = read(D / "persons.csv"), read(D / "organizations.csv"), read(D / "memberships.csv")
T = read(D / "ties.csv")
ED, C, S = read(D / "education.csv"), read(D / "candidacies.csv"), read(D / "sources.csv")
pids, oids, sids = {p["person_id"] for p in P}, {o["org_id"] for o in O}, {s["source_id"] for s in S}

print("== keys and references")
for nm, rows, key in (("persons", P, "person_id"), ("organizations", O, "org_id"), ("memberships", M, "membership_id"),
                      ("ties", T, "tie_id"), ("education", ED, "education_id"), ("candidacies", C, "candidacy_id"),
                      ("sources", S, "source_id")):
    check(len({r[key] for r in rows}) == len(rows), f"{nm}: {key} is unique ({len(rows)} rows)")
check(len({p["name"] for p in P}) == len(P), "persons: names are unique")
check(all(m["person_id"] in pids and m["org_id"] in oids for m in M), "memberships: person_id and org_id resolve")
check(all(t["person_a_id"] in pids and t["person_b_id"] in pids for t in T), "ties: both persons resolve")
check(all(r["person_id"] in pids for tab in (ED, C) for r in tab), "other tables: person_id resolves")
check(all(o["parent_org_id"] in oids | {""} for o in O), "organizations: parent_org_id resolves")
check(all(r["source_id"] in sids for tab in (M, T, ED, C) for r in tab), "source_id resolves everywhere")

check(all(c["party_org_id"] in oids for c in C if c["election_type"] == "legislative"), "candidacies: party_org_id resolves")
check(len({(c["person_id"], c["election_type"], c["election_year"], c["round"], c["position"]) for c in C}) == len(C),
      "candidacies: no duplicate person, election and round")
check(not any(o["org_id"] == "party_garda" for o in O), "organizations: Garuda held once")
check({m["role_src"] for m in M} <= {"", "reg", "news", "mem", "snapshot", "wikidata", "kemendagri", "kpu2024", "official", "profile"},
      "memberships.role_src within vocabulary")
check({p["religion"] for p in P} <= {"", "Islam", "Protestant", "Catholic", "Hindu", "Buddhist", "Confucian"},
      "persons.religion within vocabulary")
ETH = {"Javanese", "Sundanese", "Minangkabau", "Batak", "Bugis", "Madurese", "Malay", "Banjarese", "Betawi", "Balinese",
       "Acehnese", "Minahasan", "Torajan", "Mandarese", "Dayak", "Sasak", "Nias", "Lampung", "Papuan", "Indo",
       "Chinese Indonesian", "Arab Indonesian", "Indian Indonesian"}
check(all(set(filter(None, p["ethnicity"].split("; "))) <= ETH for p in P), "persons.ethnicity within vocabulary")
check(all(bool(p["ethnicity"]) == bool(p["ethnicity_src"]) and p["ethnicity_src"] in ("", "idwiki", "enwiki", "idwiki+enwiki")
          for p in P), "persons.ethnicity has a source wherever it is coded")
check({p["marital_status"] for p in P} <= {"", "married", "unmarried"}, "persons.marital_status within vocabulary")
check({p["legal_status"] for p in P} <= {"", "none_declared", "former_convict", "former_convict_on_parole",
                                         "former_convict_culpa", "convicted"}, "persons.legal_status within vocabulary")
check(all(p["n_children"].isdigit() for p in P if p["n_children"]), "persons.n_children is a whole number")
check(all(bool(p["family_legal_src"]) == any(p[c] for c in ("marital_status", "spouse_name", "n_children", "legal_status"))
          for p in P), "persons: family_legal_src set exactly where those fields are filled")
check({p["highest_degree"] for p in P} <= {"", "secondary", "diploma", "S1", "S2", "S3", "academy"},
      "persons.highest_degree within vocabulary")

print("== controlled vocabularies and formats")
V = {
    "role_level": {"head", "deputy_head", "executive_board", "regional_board", "council", "member", "not_coded"},
    "basis": {"ex_officio", "roster", "elected", "appointed", "founder", "cadre_or_member", "party_affiliation",
              "alumni", "cultural_affiliation", "owner"},
    "status_asof": {"current", "past", "unknown"},
    "src": {"reg", "news", "mem", "snapshot", "wikidata", "kemendagri", "kpu2024", "wikipedia", "official", "profile", "idnfinancials"},
    "snapshot_layer": {"", "current", "security", "advisory", "historical", "prabowo"},
    "confidence": {"", "high", "medium", "low"},
}
for col, allowed in V.items():
    bad = {m[col] for m in M} - allowed
    check(not bad, f"memberships.{col} within vocabulary" + (f" (unexpected: {bad})" if bad else ""))
DOM = {"executive", "legislature", "judiciary", "security", "advisory", "state_enterprise", "regional_government",
       "party", "campaign", "mass_organization", "business_association", "company"}
check({o["domain"] for o in O} <= DOM, "organizations.domain within vocabulary")
DATE = re.compile(r"^(\d{4}(-\d{2}(-\d{2})?)?)?$")
check(all(DATE.match(m[c]) for m in M for c in ("start_date", "end_date")), "memberships: dates are YYYY, YYYY-MM or YYYY-MM-DD")
check(all(DATE.match(p["birth_date"]) for p in P), "persons: birth_date format")
check(all(not (m["start_date"] and m["end_date"]) or m["start_date"][:4] <= m["end_date"][:4] for m in M),
      "memberships: start year is not after end year")
check(all(m["status_asof"] != "current" or not m["end_date"] for m in M), "memberships: current rows have no end date")
check({p["gender"] for p in P} <= {"", "M", "F"}, "persons.gender within vocabulary")
check({p["partisan_status"] for p in P} == {"party", "non_party", "not_coded"}, "persons.partisan_status within vocabulary")

print("== snapshot of 12 November 2026 is recoverable")
ln, la, ll = read(SNAP / "nodes.csv"), read(SNAP / "affiliations.csv"), read(SNAP / "lineage.csv")
name = {p["person_id"]: p["name"] for p in P}
snapshot_name = {o["org_id"]: o["snapshot_name"] for o in O}
seated = {m["person_id"] for m in M if m["in_snapshot"] == "1"}
snap_names = {r["Person"] for r in ln}
PS = [p for p in P if p["name"] in snap_names]          # people in the snapshot of 12 November 2026
TS = [t for t in T if t["src"] == "snapshot"]               # ties in the snapshot
rebuilt = []
for p in PS:
    sec = " ".join(x for x in (p["security_status"], p["security_service"]) if x)
    sec += f", {p['security_rank_band']} rank" if p["security_rank_band"] else ""
    i = p["person_id"]
    rebuilt.append({"Person": p["name"], "party": "non-party" if p["partisan_status"] == "non_party" else p["party_snapshot"],
                    "security_bg": sec,
                    "no_coded_seat": str(int(i not in seated))})
POOL = ("in_pool", "in_pool_expanded", "out_reason", "media_lists")   # eligibility and press lists, no longer carried in data/
check(rebuilt == [{k: v for k, v in r.items() if k not in POOL} for r in ln],
      "nodes.csv rebuilt from persons and memberships (eligibility and press list columns excepted)")
ra = [(name[m["person_id"]], snapshot_name[m["org_id"]], m["snapshot_layer"], m["src"]) for m in M if m["in_snapshot"] == "1"]
check(ra == [(a["Person"], a["Membership"], a["layer"], a["src"]) for a in la], "affiliations.csv rebuilt exactly, in order")
rl = [(name[t["person_a_id"]], name[t["person_b_id"]], t["tie_type"], t["note"], t["spec"]) for t in TS]
check(rl == [(x["a"], x["b"], x["type"], x["note"], x["spec"]) for x in ll], "lineage.csv rebuilt exactly, in order")

print("== counts of the snapshot of 12 November 2026")
L = [m for m in M if m["in_snapshot"] == "1"]
core = [m for m in L if m["snapshot_layer"] in ("current", "security")]
check((len(PS), len(L), len(TS)) == (208, 288, 26), "snapshot: 208 people, 288 affiliation rows, 26 ties")
check((len({m["person_id"] for m in core}), len({m["org_id"] for m in core})) == (142, 28), "core set: 142 people in 28 bodies")
want = {"current": (139, 24), "security": (11, 4), "advisory": (41, 3), "historical": (42, 2), "prabowo": (1, 2)}
got = {k: (len({m["person_id"] for m in L if m["snapshot_layer"] == k}), len({m["org_id"] for m in L if m["snapshot_layer"] == k})) for k in want}
check(got == want, f"people and bodies per layer {got}")
check(Counter(m["src"] for m in core) == Counter(reg=72, news=42, mem=87), "core rows by source: reg 72, news 42, mem 87")
check(len({p["person_id"] for p in PS} - seated) == 5, "5 people without a seat in the snapshot")
check(Counter(t["tie_type"] for t in TS) == Counter(kinship=15, aide=10, cohort=1), "snapshot ties: 15 kinship, 10 aide, 1 cohort")
check(Counter(t["spec"] for t in TS) == Counter(main=18, prabowo=8), "snapshot ties: 18 main, 8 prabowo")

print("== provincial governments")
prov = [o["org_id"] for o in O if o["domain"] == "regional_government"]
heads = Counter(m["org_id"] for m in M if m["org_id"] in prov and m["status_asof"] == "current" and m["role_level"] == "head"
               and "nonaktif" not in m["role"])
check(len(prov) == 38 and all(heads[o] == 1 for o in prov), "38 provinces, each with exactly one serving governor or acting governor")
check({o["org_type"] for o in O if o["domain"] == "regional_government"} == {"province"}, "regional government coded at provincial level only")

print(f"== coverage (share of the {len(P)} people with a value)")
LG = [c for c in C if c["election_type"] == "legislative"]
check(all(c["outcome"] in ("won", "lost") for c in LG) and all(bool(c["votes"]) == (c["outcome"] == "won") for c in LG),
      "legislative candidacies: outcome coded, votes present exactly for winners")
print(f"      DPR candidacies 2024: {sum(c['outcome'] == 'won' for c in LG)} won, {sum(c['outcome'] == 'lost' for c in LG)} lost")
for col in ("gender", "birth_date", "birth_place", "wikidata_qid", "religion", "ethnicity", "highest_degree", "marital_status",
            "spouse_name", "n_children", "legal_status", "pre_political_occupation"):
    print(f"      persons.{col:26s} {sum(bool(p[col]) for p in P):3d}  {sum(bool(p[col]) for p in P) / len(P):5.0%}")
dom = {o["org_id"]: o["domain"] for o in O}
new = [m for m in M if m["in_snapshot"] == "0"]
print(f"      memberships outside the snapshot: {len(new)} rows, {len({m['person_id'] for m in new})} people")
for k, v in sorted(Counter((dom[m["org_id"]], m["src"]) for m in new).items()):
    print(f"        {k[0]:22s} {k[1]:9s} {v:3d}")
print(f"      snapshot rows with a coded role: {sum(m['role_level'] != 'not_coded' for m in L)} of {len(L)}")
print(f"      people with a party row of any status: {len({m['person_id'] for m in M if dom[m['org_id']] == 'party'})}")
print(f"      people with a mass organization or business association row: {len({m['person_id'] for m in M if dom[m['org_id']] in ('mass_organization', 'business_association')})}")

if fails:
    print(f"\n{len(fails)} check(s) failed")
    sys.exit(1)
print("\nall checks passed")

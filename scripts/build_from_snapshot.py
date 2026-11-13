#!/usr/bin/env python3
"""Build the v0.1 relational tables from the snapshot and the seed files.

Inputs   data/snapshot/{nodes,affiliations,lineage}.csv   (snapshot of 12 November 2026, never edited)
         scripts/seeds/*.psv                            (pipe-separated, hand-maintained)
Outputs  data/{persons,organizations,memberships,ties,
               education,candidacies,sources}.csv

Run from the repository root:  python3 scripts/build_from_snapshot.py
The script is deterministic; running it twice gives identical files.
After v0.1 the tables in data/ are edited directly and this script is kept as the
record of how they were derived.
"""
import csv, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEG, SEED, OUT = ROOT / "data" / "snapshot", ROOT / "scripts" / "seeds", ROOT / "data"
SNAPSHOT = "2026-11-12"


def read_csv(p):
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_psv(p):
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="|", quoting=csv.QUOTE_NONE))


def write_csv(name, rows, cols):
    with open(OUT / name, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})
    print(f"{name:22s} {len(rows):4d} rows")


nodes = read_csv(LEG / "nodes.csv")
affs = read_csv(LEG / "affiliations.csv")
lin = read_csv(LEG / "lineage.csv")
orgs = read_psv(SEED / "organizations.psv")
wd = {r["name"]: r for r in read_psv(SEED / "wikidata_persons.psv")}

# ---------------------------------------------------------------- persons
pid = {r["Person"]: f"P{i:04d}" for i, r in enumerate(nodes, 1)}
SEC = re.compile(r"^(active|retired|former) (TNI|Polri)(?:, (flag|junior) rank)?$")
persons = []
for r in nodes:
    w = wd.get(r["Person"], {})
    sec = SEC.match(r["security_bg"]) if r["security_bg"] else None
    if r["security_bg"] and not sec:
        sys.exit(f"unparsed security_bg: {r['security_bg']}")
    persons.append({
        "person_id": pid[r["Person"]], "name": r["Person"],
        "gender": w.get("gender", ""), "birth_date": w.get("birth_date", ""),
        "birth_place": w.get("birth_place", ""),
        "partisan_status": "non_party" if r["party"] == "non-party" else ("party" if r["party"] else "not_coded"),
        "party_snapshot": "" if r["party"] == "non-party" else r["party"],
        "security_service": sec.group(2) if sec else "",
        "security_status": sec.group(1) if sec else "",
        "security_rank_band": (sec.group(3) or "") if sec else "",
        "wikidata_qid": w.get("wikidata_qid", ""),
        "bio_src": "wikidata" if w else "",
        # background variables defined in the codebook and not yet coded in v0.1
        "religion": "", "highest_degree": "", "degree_field": "", "studied_abroad": "",
        "pre_political_occupation": "", "political_family": "",
    })
missing = set(wd) - set(pid)
if missing:
    sys.exit(f"wikidata seed names not in nodes: {missing}")

# ---------------------------------------------------------- organizations
org_by_snapshot = {o["snapshot_name"]: o["org_id"] for o in orgs if o["snapshot_name"]}
org_ids = {o["org_id"] for o in orgs}
abbr = {o["name"]: o["org_id"] for o in orgs if o["org_type"] == "party"}
unmapped = {a["Membership"] for a in affs} - set(org_by_snapshot)
if unmapped:
    sys.exit(f"snapshot bodies without an organization record: {unmapped}")
party_of_board = {o["org_id"]: o["parent_org_id"] for o in orgs if o["org_type"] == "party_central_board"}

# ------------------------------------------------------------ memberships
M = []


def add(**k):
    k["membership_id"] = f"M{len(M) + 1:04d}"
    if k["person_id"] not in set(pid.values()) or k["org_id"] not in org_ids:
        sys.exit(f"bad reference: {k}")
    M.append(k)


BASIS = {"reg": "ex_officio", "news": "roster", "mem": "roster"}
for a in affs:
    o = org_by_snapshot[a["Membership"]]
    hist = a["layer"] == "historical"
    lead = o.startswith("leg_")
    add(person_id=pid[a["Person"]], org_id=o,
        role="Wakil Ketua" if lead else "", role_level="deputy_head" if lead else "not_coded",
        basis=BASIS[a["src"]], start_date="2023" if hist else "", end_date="2024" if hist else "",
        status_asof="past" if hist else "current", snapshot_layer=a["layer"], in_snapshot="1",
        src=a["src"], source_id="S001", confidence="",
        note="role inferred from the definition of the body" if lead else "")

# party named in nodes.csv without a seat on that party's board
for r in nodes:
    p = r["party"]
    if not p or p == "non-party":
        continue
    if p not in abbr:
        sys.exit(f"party not in organizations: {p}")
    boards = {party_of_board.get(m["org_id"]) for m in M if m["person_id"] == pid[r["Person"]]}
    other = boards - {None, abbr[p]}
    if other:
        print(f"  note: {r['Person']} has party {p} in nodes.csv and a board seat in {other}")
    if abbr[p] not in boards:
        add(person_id=pid[r["Person"]], org_id=abbr[p], role="member", role_level="member",
            basis="party_affiliation", start_date="", end_date="", status_asof="current",
            snapshot_layer="", in_snapshot="0", src="snapshot", source_id="S001", confidence="",
            note="party column of nodes.csv; no seat on the coded party board")

# roles and dates added to snapshot rows
for u in read_psv(SEED / "role_updates.psv"):
    hits = [m for m in M if m["person_id"] == pid[u["person"]] and m["org_id"] == u["org_id"]]
    if not hits:
        sys.exit(f"role update matches no row: {u}")
    for m in hits:
        for f in ("role", "role_level", "start_date", "end_date", "status_asof"):
            if u[f]:
                m[f] = u[f]
        m["role_src"], m["role_source_id"], m["confidence"] = u["src"], u["source_id"], u["confidence"]
        m["note"] = u["note"]

# new rows outside the snapshot
for s in read_psv(SEED / "memberships_seed.psv"):
    add(person_id=pid[s["person"]], org_id=s["org_id"], role=s["role"], role_level=s["role_level"],
        basis=s["basis"], start_date=s["start_date"], end_date=s["end_date"],
        status_asof=s["status_asof"] or "unknown", snapshot_layer="", in_snapshot="0",
        src=s["src"], source_id=s["source_id"], confidence=s["confidence"], note=s["note"])

# party statements from Wikidata, added only where no row links the person to that party
PAR = re.compile(r"^(.*?)(?:\((\d{4})?-(\d{4})?\))?$")
for name, w in wd.items():
    for item in filter(None, w["parties"].split(";")):
        label, start, end = PAR.match(item).groups()
        if label not in abbr:
            sys.exit(f"wikidata party not in organizations: {label}")
        party = abbr[label]
        have = {party_of_board.get(m["org_id"], m["org_id"]) for m in M if m["person_id"] == pid[name]}
        if party in have:
            continue
        add(person_id=pid[name], org_id=party, role="member", role_level="member",
            basis="party_affiliation", start_date=start or "", end_date=end or "",
            status_asof="past" if end else "unknown", snapshot_layer="", in_snapshot="0",
            src="wikidata", source_id="S003", confidence="low",
            note="Wikidata P102, not checked against a party source")

for m in M:
    m.setdefault("role_src", "")
    m.setdefault("role_source_id", "")

# ------------------------------------------------------------------ ties
ties = [{"tie_id": f"T{i:03d}", "person_a_id": pid[r["a"]], "person_b_id": pid[r["b"]],
         "tie_type": r["type"], "note": r["note"], "spec": r["spec"],
         "start_date": "", "end_date": "", "src": "snapshot", "source_id": "S001"}
        for i, r in enumerate(lin, 1)]

# ----------------------------------------- eligibility and media mentions
elig = [{"person_id": pid[r["Person"]], "rule_set": "vp_2026", "in_pool": r["in_pool"],
         "in_pool_expanded": r["in_pool_expanded"], "out_reason": r["out_reason"]} for r in nodes]
media = [{"person_id": pid[r["Person"]], "context": "vp_vacancy_2026", "as_of": SNAPSHOT,
          "n_lists": r["media_lists"], "source_id": "S001"} for r in nodes if int(r["media_lists"]) > 0]

# -------------------------------------------------- education, candidacies
edu = [{"education_id": f"E{i:03d}", "person_id": pid[r["person"]], **{k: r[k] for k in
        ("institution", "institution_type", "level", "grad_year", "src", "source_id", "confidence", "note")},
        "field": "", "country": "ID"} for i, r in enumerate(read_psv(SEED / "education_seed.psv"), 1)]
cand = [{"candidacy_id": f"C{i:03d}", "person_id": pid[r["person"]], "election_type": "presidential",
         **{k: r[k] for k in ("election_year", "round", "position", "running_mate", "vote_share_pct",
                              "outcome", "src", "source_id", "confidence")}}
        for i, r in enumerate(read_psv(SEED / "candidacies_seed.psv"), 1)]

# ----------------------------------------------------------------- write
write_csv("persons.csv", persons, list(persons[0]))
write_csv("organizations.csv", orgs, ["org_id", "name", "name_long", "domain", "org_type",
                                      "parent_org_id", "stream", "snapshot_name", "note"])
write_csv("memberships.csv", M, ["membership_id", "person_id", "org_id", "role", "role_level", "basis",
                                 "start_date", "end_date", "status_asof", "snapshot_layer",
                                 "in_snapshot", "src", "source_id", "role_src", "role_source_id",
                                 "confidence", "note"])
write_csv("ties.csv", ties, list(ties[0]))
# eligibility.csv was removed from the dataset in version 0.2 and is no longer written
# media_mentions.csv was removed from the dataset and is no longer written
write_csv("education.csv", edu, ["education_id", "person_id", "institution", "institution_type", "level",
                                 "field", "grad_year", "country", "src", "source_id", "confidence", "note"])
write_csv("candidacies.csv", cand, ["candidacy_id", "person_id", "election_type", "election_year", "round",
                                    "position", "running_mate", "vote_share_pct", "outcome", "src",
                                    "source_id", "confidence"])
write_csv("sources.csv", read_psv(SEED / "sources.psv"),
          ["source_id", "type", "title", "publisher", "url", "date_published", "date_retrieved", "note"])

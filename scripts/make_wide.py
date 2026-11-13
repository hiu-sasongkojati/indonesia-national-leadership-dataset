#!/usr/bin/env python3
"""Derive the one-row-per-person table from the relational tables in data/.

Outputs  derived/persons_wide.csv          one row per person, one column per affiliation domain
         derived/memberships_labeled.csv   memberships with names instead of identifiers

Run from the repository root:  python3 scripts/make_wide.py
Never edit the files in derived/ by hand; edit data/ and run this script again.
"""
import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D, OUT = ROOT / "data", ROOT / "derived"
OUT.mkdir(exist_ok=True)


def read(name):
    with open(D / name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write(name, rows, cols):
    with open(OUT / name, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader()
        w.writerows({c: r.get(c, "") for c in cols} for r in rows)
    print(f"{name:26s} {len(rows):4d} rows, {len(cols)} columns")


P, O, M = read("persons.csv"), {o["org_id"]: o for o in read("organizations.csv")}, read("memberships.csv")
name = {p["person_id"]: p["name"] for p in P}
by = defaultdict(list)
for m in M:
    by[m["person_id"]].append(m)


def span(m):
    s, e = m["start_date"], m["end_date"]
    if not s and not e:
        return ""
    return f"{s or '?'}–{e or ('' if m['status_asof'] == 'current' else '?')}"


def label(m, with_status=True):
    o = O[m["org_id"]]
    parts = [m["role"], o["name"]] if m["role"] and m["role"] != "member" else [o["name"]]
    tail = [x for x in (span(m), m["status_asof"] if with_status and m["status_asof"] != "current" else "") if x]
    return ", ".join(parts) + (f" ({'; '.join(tail)})" if tail else "")


def party_of(m):
    o = O[m["org_id"]]
    return O[o["parent_org_id"]]["name"] if o["org_type"] == "party_central_board" else o["name"]


def pick(ms, domain=None, types=None, status=None):
    out = []
    for m in ms:
        o = O[m["org_id"]]
        if domain and o["domain"] != domain:
            continue
        if types and not any(o["org_type"].startswith(t) for t in types):
            continue
        if status == "current" and m["status_asof"] != "current":
            continue
        if status == "not_current" and m["status_asof"] == "current":
            continue
        out.append(m)
    return out


def best_per_party(ms):
    """One entry per party; where several rows name the same party, keep the one with the fuller dates."""
    out = {}
    for m in ms:
        txt = "; ".join(x for x in (span(m), m["status_asof"]) if x)
        k = party_of(m)
        if k not in out or (m["start_date"] and "?–" in out[k]) or len(txt) > len(out[k]) and "?–" not in txt:
            out[k] = txt
    return out


J = "; ".join
ties, edu, cand = read("ties.csv"), read("education.csv"), read("candidacies.csv")

rows = []
for p in P:
    i, ms = p["person_id"], by[p["person_id"]]
    cur_party = pick(ms, "party", status="current")
    cur_names = sorted({party_of(m) for m in cur_party})
    other = [m for m in pick(ms, "party", status="not_current") if party_of(m) not in cur_names]
    sec = " ".join(x for x in (p["security_status"], p["security_service"]) if x)
    if p["security_rank_band"]:
        sec += f", {p['security_rank_band']} rank"
    t = defaultdict(list)
    for x in ties:
        if i in (x["person_a_id"], x["person_b_id"]):
            other_id = x["person_b_id"] if x["person_a_id"] == i else x["person_a_id"]
            t[x["tie_type"]].append(f"{name[other_id]} ({x['note']})")
    snapshot = [m for m in ms if m["in_snapshot"] == "1"]
    rows.append({
        "person_id": i, "name": p["name"], "gender": p["gender"], "birth_date": p["birth_date"],
        "birth_year": p["birth_date"][:4], "birth_place": p["birth_place"],
        "religion": p["religion"], "ethnicity": p["ethnicity"], "highest_degree": p["highest_degree"],
        "marital_status": p["marital_status"], "spouse_name": p["spouse_name"], "n_children": p["n_children"],
        "legal_status": p["legal_status"],
        "partisan_status": p["partisan_status"],
        "party_current": J(cur_names) or ("non-party" if p["partisan_status"] == "non_party" else ""),
        "party_role_current": J(f"{m['role']} ({party_of(m)})" for m in cur_party if m["role"] not in ("", "member")),
        "party_other": J(f"{k} ({v})" for k, v in sorted(best_per_party(other).items())),
        "executive_current": J(label(m) for m in pick(ms, "executive", status="current")),
        "legislature_current": J(label(m) for m in pick(ms, "legislature", status="current")),
        "security_current": J(label(m) for m in pick(ms, "security", status="current")),
        "advisory_current": J(label(m) for m in pick(ms, "advisory", status="current")),
        "state_enterprise_current": J(label(m) for m in pick(ms, "state_enterprise", status="current")),
        "regional_current": J(label(m) for m in pick(ms, "regional_government", status="current")),
        "offices_past": J(label(m) for d in ("executive", "regional_government", "judiciary", "legislature")
                          for m in pick(ms, d, status="not_current")),
        "campaign_2024": J(O[m["org_id"]]["name"] + (f" [{m['role']}]" if m["role"] else "") for m in pick(ms, "campaign")),
        "ormas_religious": J(label(m) for m in pick(ms, "mass_organization", types=["religious"])),
        "ormas_student_youth": J(label(m) for m in pick(ms, "mass_organization", types=["student", "youth"])),
        "ormas_other": J(label(m) for m in pick(ms, "mass_organization", types=["labour", "veterans", "sports", "farmers"])),
        "business_assoc": J(label(m) for m in pick(ms, "business_association")),
        "company_board": J(label(m) for m in pick(ms, "company") if m["basis"] != "owner"),
        "company_ownership": J(label(m) for m in pick(ms, "company") if m["basis"] == "owner"),
        "security_bg": sec,
        "academy_cohort": J(f"{x['institution']} {x['grad_year']}" for x in edu
                            if x["person_id"] == i and x["institution_type"].endswith("academy")),
        "kin_ties": J(t["kinship"]), "aide_ties": J(t["aide"]), "cohort_ties": J(t["cohort"]),
        "presidential_candidacies": J(f"{c['election_year']} r{c['round']} {c['position']} ({c['outcome']}, {c['vote_share_pct']}%)"
                                      for c in cand if c["person_id"] == i and c["election_type"] == "presidential"),
        "dpr_candidacy_2024": J(f"{O[c['party_org_id']]['name']}, {c['constituency']}, list no. {c['list_number']}"
                                + (f", {c['outcome']}" if c["outcome"] else "") + (f" ({int(c['votes']):,} votes)" if c.get("votes") else "")
                                for c in cand if c["person_id"] == i and c["election_type"] == "legislative"
                                and c["election_year"] == "2024"),
        "n_snapshot_seats": len(snapshot),
        "n_core_seats": sum(m["snapshot_layer"] in ("current", "security") for m in snapshot),
        "no_current_seat": int(not any(m["status_asof"] == "current" and m["role"] != "member" for m in ms)
                               and not any(m["status_asof"] == "current" and m["snapshot_layer"] for m in ms)),
        "wikidata_qid": p["wikidata_qid"],
    })
write("persons_wide.csv", rows, list(rows[0]))

lab = [{**m, "person": name[m["person_id"]], "organization": O[m["org_id"]]["name"],
        "domain": O[m["org_id"]]["domain"], "org_type": O[m["org_id"]]["org_type"]} for m in M]
write("memberships_labeled.csv", lab, ["membership_id", "person", "organization", "domain", "org_type", "role",
                                       "role_level", "basis", "start_date", "end_date", "status_asof",
                                       "snapshot_layer", "in_snapshot", "src", "role_src", "confidence", "note"])

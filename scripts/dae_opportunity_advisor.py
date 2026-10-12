"""Evidence-first advice layer for DAE hourly leads. Stdlib only; no task execution."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

UNSAFE = re.compile(r"\b(upfront fee|pay to apply|seed phrase|private key|connect your wallet|deposit first|unpaid|no payment)\b", re.I)
MONEY_TERMS = re.compile(r"\b(funded|escrow|sponsor|budget|payout|paid|reward|bounty|payment)\b", re.I)


def assess(lead):
    reasons = list(lead.get("reasons") or [])
    title = str(lead.get("title") or "")
    url = str(lead.get("url") or "")
    amount = lead.get("reward_amount_claimed_usd")
    deadline = lead.get("deadline_text")
    status = str(lead.get("review_status") or "")
    repo = str(lead.get("repository") or "")
    author = str(lead.get("author") or "")
    updated = str(lead.get("updated_at") or "")
    text = title + " " + " ".join(reasons)
    unsafe = bool(UNSAFE.search(text))
    payment_confidence = 0
    evidence = []
    if amount is not None and amount > 0:
        evidence.append("A positive reward amount is stated; this is not proof of funding.")
        payment_confidence += 10
    else:
        evidence.append("Reward amount missing, ambiguous, zero or invalid.")
    if deadline:
        evidence.append("Deadline text found; verify timezone and whether it is still open.")
        payment_confidence += 10
    else:
        evidence.append("No explicit deadline detected.")
    if repo:
        evidence.append("Repository/source metadata is present; organizer identity still needs independent review.")
    if updated:
        evidence.append("Source update timestamp is present; check freshness and whether the opportunity remains open.")
    payment_confidence = min(payment_confidence, 20)

    risks = [
        "Funding is UNVERIFIED: no independent proof of reserved funds was collected.",
        "Eligibility, location/age restrictions and complete terms require manual review.",
        "Acceptance criteria and judging discretion are not sufficiently structured in this source snapshot.",
        "Competitor count and existing submissions are unknown; numeric win probability would be misleading.",
    ]
    if unsafe:
        risks.insert(0, "Potentially unsafe or explicitly unpaid language detected; do not proceed unless primary-source review resolves it.")
    if status != "REVIEW_LEAD":
        risks.append("Scanner flagged this lead for manual checks: " + "; ".join(reasons))
    if amount is not None and amount > 0:
        net = "NOT ESTIMABLE — effort, fees, payout probability and funding are unverified"
    else:
        net = "NOT ESTIMABLE — reward, effort, fees, payout probability and funding are unknown"

    if unsafe:
        recommendation = "REJECT / AVOID unless official primary-source evidence clearly resolves the safety flag."
        tier = "AVOID"
    elif amount is not None and amount > 0 and deadline and status == "REVIEW_LEAD":
        recommendation = "RESEARCH FURTHER — verify funder, enforceable payment terms, eligibility, deadline and competition before investing time."
        tier = "REVIEW"
    elif amount is not None and amount > 0:
        recommendation = "LOW PRIORITY — key terms/evidence missing; verify before doing work."
        tier = "LOW"
    else:
        recommendation = "HOLD — no sufficiently concrete reward evidence; inspect official source before considering it."
        tier = "HOLD"

    # This is a triage score only; it is not probability of winning or being paid.
    triage_score = 0
    triage_score += 25 if amount is not None and amount > 0 else 0
    triage_score += 20 if deadline else 0
    triage_score += 15 if status == "REVIEW_LEAD" else 0
    triage_score += 10 if repo else 0
    triage_score += 5 if updated else 0
    if unsafe:
        triage_score = 0
    return {
        "id": lead.get("id"), "title": title, "url": url,
        "repository": repo, "author": author,
        "claimed_reward_usd": amount,
        "deadline_text": deadline,
        "source_updated_at": updated,
        "funding_status": "UNVERIFIED",
        "payment_confidence_score": payment_confidence,
        "payment_confidence_note": "0–20 evidence-completeness heuristic, not a probability of being paid.",
        "triage_score": triage_score,
        "triage_score_note": "0–75 lead-completeness score for review ordering only; not payment confidence or win probability.",
        "triage_tier": tier,
        "win_potential": "UNRATED — insufficient competition and judging data",
        "estimated_net_value_per_hour": net,
        "participation_checklist": [
            "Open the original issue and follow links to official rules/terms.",
            "Verify organizer/funder identity and independently confirm reserved funds or enforceable payout terms.",
            "Check deadline, timezone, eligibility, geography and age requirements.",
            "Read acceptance criteria; inspect current competitors/submissions and winner-selection rules.",
            "Estimate hours, fees and opportunity cost; never pay upfront or share secrets.",
            "Save official terms and evidence timestamps before deciding.",
        ],
        "risks": risks,
        "recommendation": recommendation,
        "evidence_notes": evidence,
    }


def main():
    reports = Path("reports")
    source = reports / "hourly_latest.json"
    if not source.exists():
        raise SystemExit("Missing reports/hourly_latest.json; run the read-only scanner first.")
    payload = json.loads(source.read_text(encoding="utf-8"))
    results = [assess(x) for x in payload.get("results", [])]
    results.sort(key=lambda x: (x["triage_tier"] == "REVIEW", x["triage_score"], x["claimed_reward_usd"] or 0), reverse=True)
    generated = datetime.now(timezone.utc).isoformat()
    counts = {tier: sum(1 for item in results if item["triage_tier"] == tier) for tier in ("REVIEW", "LOW", "HOLD", "AVOID")}
    report = {
        "schema_version": "0.8.1",
        "generated_at": generated,
        "source_report_generated_at": payload.get("generated_at"),
        "summary": {
            "assessed_leads": len(results),
            "triage_counts": counts,
            "verified_funding_count": 0,
            "numeric_win_probability_count": 0,
            "warning": "No funding is independently verified by this heuristic-only layer.",
        },
        "results": results,
    }
    (reports / "hourly_advice.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# DAE Opportunity Brief", "",
        f"Generated: {generated}",
        f"Leads assessed: {len(results)} | Verified funding: 0 | Numeric win probabilities: 0",
        f"Triage counts: {counts}", "",
        "> All listed rewards are UNVERIFIED until independently confirmed. Triage scores are not probabilities and this report does not guarantee payment or winning.", "",
    ]
    if not results:
        lines.append("No leads found in the latest scan.")
    for i, item in enumerate(results, 1):
        lines += [
            f"## {i}. [{item['triage_tier']}] {item['title'] or '(untitled lead)'}",
            f"- Source: {item['url']}",
            f"- Claimed reward: {item['claimed_reward_usd'] if item['claimed_reward_usd'] is not None else 'UNVERIFIED / not stated'}",
            f"- Funding: **UNVERIFIED** | Evidence completeness: {item['payment_confidence_score']}/20",
            f"- Triage score: {item['triage_score']}/75 (not a probability)",
            f"- Win potential: {item['win_potential']}",
            f"- Net value/hour: {item['estimated_net_value_per_hour']}",
            f"- Recommendation: {item['recommendation']}",
            "- Participation checklist:",
        ]
        lines += [f"  - {x}" for x in item["participation_checklist"]]
        lines += ["- Risks:"] + [f"  - {x}" for x in item["risks"]] + [""]
    (reports / "hourly_opportunity_brief.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"DAE advisor: assessed={len(results)} verified_funding=0 triage_counts={counts}")
    print("Reports: reports/hourly_advice.json and reports/hourly_opportunity_brief.md")


if __name__ == "__main__":
    main()

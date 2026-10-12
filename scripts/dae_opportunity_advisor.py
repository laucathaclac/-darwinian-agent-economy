"""Evidence-first advice layer for DAE hourly leads. Stdlib only; no task execution."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

MONEY_TERMS = re.compile(r"\b(funded|escrow|sponsor|budget|payout|paid|reward|bounty|payment)\b", re.I)
UNSAFE = re.compile(r"\b(upfront fee|pay to apply|seed phrase|private key|connect your wallet|deposit first)\b", re.I)

def assess(lead):
    reasons = list(lead.get("reasons") or [])
    title = str(lead.get("title") or "")
    url = str(lead.get("url") or "")
    amount = lead.get("reward_amount_claimed_usd")
    deadline = lead.get("deadline_text")
    status = str(lead.get("review_status") or "")
    # A listing's own text is not independent proof that funds exist.
    payment_confidence = 0
    evidence = []
    if amount is not None:
        evidence.append("A reward amount is stated; this is not proof of funding.")
        payment_confidence += 10
    else:
        evidence.append("Reward amount missing or ambiguous.")
    if deadline:
        evidence.append("Deadline text found; verify timezone and whether it is still open.")
        payment_confidence += 10
    else:
        evidence.append("No explicit deadline detected.")
    payment_confidence = min(payment_confidence, 20)
    risks = [
        "Funding is UNVERIFIED: no independent proof of reserved funds was collected.",
        "Eligibility, location/age restrictions and complete terms require manual review.",
        "Acceptance criteria and judging discretion are not sufficiently structured in this source snapshot.",
        "Competitor count and existing submissions are unknown; a numeric win probability would be misleading.",
    ]
    if UNSAFE.search(title + " " + " ".join(reasons)):
        risks.insert(0, "Potentially unsafe payment/wallet language detected; avoid unless independently cleared.")
    if status != "REVIEW_LEAD":
        risks.append("Scanner flagged this lead for manual checks: " + "; ".join(reasons))
    if amount is not None:
        net = "NOT ESTIMABLE — effort, fees, payout probability and funding are unverified"
    else:
        net = "NOT ESTIMABLE — reward, effort, fees, payout probability and funding are unknown"
    # Conservative recommendation is based on evidence completeness, not headline reward.
    if amount is not None and deadline and status == "REVIEW_LEAD":
        recommendation = "RESEARCH FURTHER — verify funder, escrow/payment terms, eligibility and competition before investing time."
        win_potential = "UNRATED — insufficient competition and judging data"
    elif amount is not None:
        recommendation = "LOW PRIORITY — key terms/evidence missing; verify before doing work."
        win_potential = "UNRATED — insufficient evidence"
    else:
        recommendation = "HOLD / REJECT unless primary-source review supplies concrete payment terms."
        win_potential = "UNRATED — insufficient evidence"
    return {
        "id": lead.get("id"), "title": title, "url": url,
        "claimed_reward_usd": amount,
        "funding_status": "UNVERIFIED",
        "payment_confidence_score": payment_confidence,
        "payment_confidence_note": "0–20 evidence completeness heuristic, not a probability of being paid.",
        "win_potential": win_potential,
        "estimated_net_value_per_hour": net,
        "participation_checklist": [
            "Read official rules and acceptance criteria end to end.",
            "Verify organizer/funder identity and independently confirm funds are reserved or payout terms are enforceable.",
            "Check deadline, timezone, eligibility, geography and any age requirements.",
            "Inspect current competitors/submissions and how winners are selected.",
            "Estimate hours, fees and opportunity cost; do not pay upfront or share secrets.",
            "Save official terms and evidence timestamps before deciding."
        ],
        "risks": risks,
        "recommendation": recommendation,
        "evidence_notes": evidence,
        "source_updated_at": lead.get("updated_at"),
    }

def main():
    reports = Path("reports")
    source = reports / "hourly_latest.json"
    if not source.exists():
        raise SystemExit("Missing reports/hourly_latest.json; run the read-only scanner first.")
    payload = json.loads(source.read_text(encoding="utf-8"))
    results = [assess(x) for x in payload.get("results", [])]
    # Order by evidence completeness first, then a claimed amount only as a tiebreaker.
    results.sort(key=lambda x: (x["payment_confidence_score"], x["claimed_reward_usd"] or 0), reverse=True)
    generated = datetime.now(timezone.utc).isoformat()
    report = {
        "schema_version": "0.8",
        "generated_at": generated,
        "source_report_generated_at": payload.get("generated_at"),
        "summary": {
            "assessed_leads": len(results),
            "verified_funding_count": 0,
            "numeric_win_probability_count": 0,
            "warning": "No funding is independently verified by this heuristic-only layer."
        },
        "results": results,
    }
    (reports / "hourly_advice.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# DAE Opportunity Brief",
        "",
        f"Generated: {generated}",
        f"Leads assessed: {len(results)} | Independently verified funding: 0 | Numeric win probabilities: 0",
        "",
        "> All listed rewards are UNVERIFIED until independently confirmed. This report does not guarantee payment or winning.",
        "",
    ]
    if not results:
        lines.append("No leads found in the latest scan.")
    for i, item in enumerate(results, 1):
        lines += [
            f"## {i}. {item['title'] or '(untitled lead)'}",
            f"- Source: {item['url']}",
            f"- Claimed reward: {item['claimed_reward_usd'] if item['claimed_reward_usd'] is not None else 'UNVERIFIED / not stated'}",
            f"- Funding: **UNVERIFIED** | Payment evidence score: {item['payment_confidence_score']}/20",
            f"- Win potential: {item['win_potential']}",
            f"- Net value/hour: {item['estimated_net_value_per_hour']}",
            f"- Recommendation: {item['recommendation']}",
            "- Participation checklist:",
        ]
        lines += [f"  - {x}" for x in item["participation_checklist"]]
        lines += ["- Risks:"] + [f"  - {x}" for x in item["risks"]]
        lines += ["",]
    (reports / "hourly_opportunity_brief.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"DAE advisor: assessed={len(results)} verified_funding=0")
    print("Reports: reports/hourly_advice.json and reports/hourly_opportunity_brief.md")

if __name__ == "__main__":
    main()

"""Generate free, read-only search links for opportunities beyond GitHub."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

QUERIES = [
    ("X", "Paid coding and issue bounties", '("bounty" OR "paid issue" OR "reward") (developer OR coding OR GitHub)', "Public posts advertising software tasks and bounties."),
    ("X", "Freelance micro-projects", '("paid task" OR "freelance" OR "contract") (developer OR Python OR frontend)', "Short coding contracts; verify payment and eligibility."),
    ("X", "Creator campaigns and writing rewards", '("creator campaign" OR "writing contest" OR "content rewards") (crypto OR Web3)', "Creator campaigns; token prizes are not cash unless terms say so."),
    ("Web search → Binance Square", "Binance Square creator campaigns", 'site:binance.com/en/square "campaign" ("reward" OR "prize" OR "creator")', "Public web-indexed campaign posts; check current terms."),
    ("Web search → Binance Square", "Binance Square writing contests", 'site:binance.com/en/square ("writing contest" OR "content challenge" OR "creator challenge")', "Find contest terms and confirm eligibility."),
    ("Web search → wider bounty ecosystem", "Web3 and open-source bounties", '("bounty" OR "grant" OR "hackathon") ("reward pool" OR "paid") (developer OR open source OR Web3)', "Broader programs beyond GitHub Issues."),
]

def build_report():
    results = []
    for source, category, query, why in QUERIES:
        host = "https://x.com/search?q=" if source == "X" else "https://www.google.com/search?q="
        results.append({"source": source, "category": category, "query": query,
                        "url": host + quote_plus(query), "why": why})
    return {"schema_version": "0.9", "generated_at": datetime.now(timezone.utc).isoformat(),
            "mode": "manual_review_links_only", "paid_api_calls": 0, "live_results_fetched": 0,
            "results": results,
            "warning": "These are discovery links, not verified opportunities. No offer, funding, reward, eligibility, or payout has been verified. Never pay upfront fees."}

def main():
    out = Path(os.environ.get("DAE_REPORT_DIR", "reports"))
    out.mkdir(parents=True, exist_ok=True)
    report = build_report()
    (out / "external_source_searches.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    lines = ["# DAE v0.9 — External Opportunity Discovery", "", f"Generated: {report['generated_at']}", "",
             "**Mode:** free search links only; no paid API calls and no scraping.", "",
             "> These are leads, not verified rewards. Check official funding, terms, deadline, acceptance criteria, age/location eligibility, and payout method. Token prizes are not cash. Never pay to apply or reveal wallet secrets.", ""]
    for i, item in enumerate(report["results"], 1):
        lines.extend([f"## {i}. {item['category']}", f"- Source: {item['source']}", f"- Search: {item['query']}",
                      f"- Why: {item['why']}", f"- Open search: {item['url']}", ""])
    (out / "external_source_searches.md").write_text("\\n".join(lines), encoding="utf-8")
    print(f"DAE external discovery links: {len(report['results'])}")
    print("Live offers verified: 0 | Paid API calls: 0")
    print(f"Reports: {out / 'external_source_searches.md'} and {out / 'external_source_searches.json'}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

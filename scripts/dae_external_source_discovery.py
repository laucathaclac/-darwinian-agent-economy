"""Generate free, official-platform search links for opportunities beyond GitHub.

This module does not scrape pages or call paid APIs. It creates review links for
X and web-indexed Binance Square/campaign posts so a human can verify the offer.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

SEARCHES = [
    {
        "source": "X",
        "category": "paid coding and issue bounties",
        "query": '("bounty" OR "paid issue" OR "reward") (developer OR coding OR GitHub)',
        "url": "https://x.com/search?q=" + quote_plus('("bounty" OR "paid issue" OR "reward") (developer OR coding OR GitHub)'),
        "why": "Finds public posts advertising software tasks and bounties.",
    },
    {
        "source": "X",
        "category": "freelance micro-projects",
        "query": '("paid task" OR "freelance" OR "contract") (developer OR Python OR frontend)',
        "url": "https://x.com/search?q=" + quote_plus('("paid task" OR "freelance" OR "contract") (developer OR Python OR frontend)'),
        "why": "Surfaces short coding contracts; payment and eligibility still need review.",
    },
    {
        "source": "X",
        "category": "creator campaigns and writing rewards",
        "query": '("creator campaign" OR "writing contest" OR "content rewards") (crypto OR Web3)',
        "url": "https://x.com/search?q=" + quote_plus('("creator campaign" OR "writing contest" OR "content rewards") (crypto OR Web3)'),
        "why": "Finds creator campaigns; token prizes are not counted as cash unless terms prove a cash payout.",
    },
    {
        "source": "Web search → Binance Square",
        "category": "Binance Square creator campaigns",
        "query": 'site:binance.com/en/square "campaign" ("reward" OR "prize" OR "creator")',
        "url": "https://www.google.com/search?q=" + quote_plus('site:binance.com/en/square "campaign" ("reward" OR "prize" OR "creator")'),
        "why": "Uses a public web search instead of an undocumented Square API or page scraping.",
    },
    {
        "source": "Web search → Binance Square",
        "category": "Binance Square writing contests",
        "query": 'site:binance.com/en/square ("writing contest" OR "content challenge" OR "creator challenge")',
        "url": "https://www.google.com/search?q=" + quote_plus('site:binance.com/en/square ("writing contest" OR "content challenge" OR "creator challenge")'),
        "why": "Looks for public contest terms; check whether the campaign is current and whether the user is eligible.",
    },
    {
        "source": "Web search → wider bounty ecosystem",
        "category": "Web3 and open-source bounties",
        "query": '("bounty" OR "grant" OR "hackathon") ("reward pool" OR "paid") (developer OR open source OR Web3)',
        "url": "https://www.google.com/search?q=" + quote_plus('("bounty" OR "grant" OR "hackathon") ("reward pool" OR "paid") (developer OR open source OR Web3)'),
        "why": "Expands beyond GitHub issues to program pages and hackathons.",
    },
]

def build_report():
    return {
        "schema_version": "0.9",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "manual_review_links_only",
        "paid_api_calls": 0,
        "live_results_fetched": 0,
        "results": SEARCHES,
        "warning": (
            "These are discovery links, not verified opportunities. No offer, funding, "
            "reward, eligibility, or payout has been verified. Do not pay upfront fees."
        ),
    }

def main():
    out = Path(os.environ.get("DAE_REPORT_DIR", "reports"))
    out.mkdir(parents=True, exist_ok=True)
    report = build_report()
    (out / "external_source_searches.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# DAE v0.9 — External Opportunity Discovery",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "**Mode:** free search links only; no paid API calls and no scraping.",
        "",
        "> These links are leads, not verified rewards. Confirm official terms, funding,",
        "> deadline, acceptance criteria, location/age eligibility, and payout method.",
        "> Token prizes are not cash. Never pay to apply or connect a wallet to claim a prize.",
        "",
    ]
    for i, item in enumerate(SEARCHES, 1):
        lines += [
            f"## {i}. {item['category']}",
            f"- Source: {item['source']}",
            f"- Search: {item['query']}",
            f"- Why: {item['why']}",
            f"- Open search: {item['url']}",
            "",
        ]
    (out / "external_source_searches.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"DAE external discovery links: {len(SEARCHES)}")
    print("Live offers verified: 0 | Paid API calls: 0")
    print(f"Reports: {out / 'external_source_searches.md'} and {out / 'external_source_searches.json'}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

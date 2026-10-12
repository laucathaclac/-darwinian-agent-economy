"""Free, read-only hourly lead scanner. Standard library only; no task execution."""
import json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

API = "https://api.github.com/search/issues"
QUERIES = {
    "coding": ['"bounty" "paid"', '"bug bounty"', '"reward" "pull request"', '"paid issue"'],
    "freelance": ['"freelance" "paid"', '"contract" "payment"', '"paid task"', '"compensation" "deadline"'],
}
MONEY = re.compile(r'(?<!\w)\$\s*([0-9][0-9,]*(?:\.\d{1,2})?)\b|\bUSD\s*([0-9][0-9,]*(?:\.\d{1,2})?)\b', re.I)
POSITIVE = re.compile(r'\b(reward|bounty|paid|payment|compensation|payout|budget)\b', re.I)
NEGATIVE = re.compile(r'\b(unpaid|no\s+(?:reward|bounty|payment|payout)|not\s+guaranteed|pay\s+to\s+apply|upfront\s+fee|seed\s+phrase|private\s+key|connect\s+(?:your\s+)?wallet|deposit\s+first|send\s+crypto\s+first)\b', re.I)

def fetch(query, limit=20):
    params = urlencode({"q": f"is:issue is:open {query}", "per_page": min(100, max(1, limit)), "sort": "updated", "order": "desc"})
    req = Request(API + "?" + params, headers={"Accept":"application/vnd.github+json","User-Agent":"DAE-hourly-readonly/0.8","X-GitHub-Api-Version":"2022-11-28"}, method="GET")
    try:
        with urlopen(req, timeout=12) as response:
            if response.status != 200: raise RuntimeError(f"GitHub HTTP {response.status}")
            payload=json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        if exc.code == 403 and exc.headers.get("X-RateLimit-Remaining") == "0": raise RuntimeError("GitHub rate limit reached; try next hour")
        raise RuntimeError(f"GitHub HTTP {exc.code}") from exc
    except (URLError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise RuntimeError(f"GitHub request failed safely: {exc}") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list): raise RuntimeError("Unexpected GitHub response")
    return payload["items"]

def evaluate(item):
    title=str(item.get("title") or "")
    body=str(item.get("body") or "")
    text=title+"\n"+body
    reasons=[]
    if item.get("pull_request") is not None: reasons.append("pull request, not an offer")
    if NEGATIVE.search(text): reasons.append("unpaid/unsafe fee language; manual check")
    if not POSITIVE.search(text): reasons.append("no payment-related wording")
    amounts=[]
    for match in MONEY.finditer(text):
        token=next((g for g in match.groups() if g), None)
        if token:
            try: amounts.append(float(token.replace(",","")))
            except ValueError: pass
    amount=amounts[0] if len(set(amounts)) == 1 and amounts else None
    if amount is None: reasons.append("reward amount missing or ambiguous")
    deadline=re.search(r'(?im)^\s*(?:deadline|due date|submit by|closes)\s*[:\-]\s*(.+)$', body)
    if not deadline: reasons.append("explicit deadline not found")
    return {
      "id": str(item.get("id") or item.get("html_url") or ""),
      "title": title, "url": str(item.get("html_url") or ""),
      "repository": "/".join(str(item.get("repository_url") or "").rstrip("/").split("/")[-2:]),
      "author": str((item.get("user") or {}).get("login") or ""),
      "updated_at": str(item.get("updated_at") or ""),
      "reward_amount_claimed_usd": amount,
      "reward_status": "UNVERIFIED — GitHub text is not proof of funding",
      "deadline_text": deadline.group(1).strip() if deadline else None,
      "review_status": "REVIEW_LEAD" if not reasons else "NEEDS_MANUAL_CHECK",
      "reasons": reasons,
      "manual_checks": ["confirm funder and that funds are actually reserved", "read full terms and acceptance criteria", "check age, location and eligibility", "never pay an upfront fee"]
    }

def main():
    profile=os.environ.get("DAE_PROFILE","both")
    limit=int(os.environ.get("DAE_LIMIT","25"))
    out=Path(os.environ.get("DAE_REPORT_DIR","reports")); out.mkdir(parents=True, exist_ok=True)
    if profile not in QUERIES and profile != "both": print("DAE_PROFILE must be coding, freelance, or both",file=sys.stderr); return 2
    keys=list(QUERIES) if profile=="both" else [profile]
    old_path=out/"hourly_seen.json"
    try: old=set(json.loads(old_path.read_text(encoding="utf-8")).get("seen",[])) if old_path.exists() else set()
    except (OSError,ValueError,AttributeError): old=set()
    leads={}
    try:
        for key in keys:
            for q in QUERIES[key]:
                for item in fetch(q, max(10, limit//(len(keys)*4))):
                    lead=evaluate(item)
                    if lead["url"]: leads[lead["url"]]=lead
    except RuntimeError as exc: print(f"DAE scan stopped safely: {exc}",file=sys.stderr); return 2
    ordered=sorted(leads.values(),key=lambda x:(x["review_status"]=="REVIEW_LEAD",x["reward_amount_claimed_usd"] or 0,x["updated_at"]),reverse=True)[:limit]
    stamp=datetime.now(timezone.utc).isoformat()
    ids={x["url"] for x in ordered if x["url"]}
    new=[x for x in ordered if x["url"] not in old]
    report={"schema_version":"0.8","generated_at":stamp,"profile":profile,"results":ordered,"new_count":len(new),"verified_funded_count":0,"warning":"All reward claims remain unverified until a human confirms actual funding. Read-only only; no task accepted, contacted, executed, or submitted."}
    (out/"hourly_latest.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (out/"hourly_new_leads.json").write_text(json.dumps({"generated_at":stamp,"new_count":len(new),"results":new},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (out/"hourly_seen.json").write_text(json.dumps({"updated_at":stamp,"seen":sorted(old|ids)[-5000:]},indent=2),encoding="utf-8")
    try:
        with (out/"hourly.log").open("a",encoding="utf-8") as f:
            f.write(f"{stamp} results={len(ordered)} new={len(new)} verified_funded=0\n")
    except OSError as exc:
        # Reports are the primary output; a locked log must not invalidate them.
        print(f"Warning: could not append hourly.log: {exc}",file=sys.stderr)
    print(f"DAE read-only scan: results={len(ordered)} new={len(new)} verified_funded=0")
    print(f"Reports: {out/'hourly_latest.json'} and {out/'hourly_new_leads.json'}")
    return 0
if __name__ == "__main__": raise SystemExit(main())

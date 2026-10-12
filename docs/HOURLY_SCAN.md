# DAE hourly paid-project discovery

The scanner runs on free public GitHub Issues search, via GET-only requests, once per invocation. On Windows, run scripts/SETUP_HOURLY_TASK.bat to schedule scripts/RUN_HOURLY_SCAN.bat every hour. Output is saved in reports/hourly_latest.json, reports/hourly_new_leads.json, reports/hourly_seen.json, and reports/hourly.log.

GitHub is an issue tracker, not a complete freelance marketplace. Search hits are leads only. The scanner never treats text mentioning a reward as proof of funded money: verified_funded_count is always 0 until a human checks funding outside this tool. Check terms, eligibility, deadline, acceptance criteria, client identity and actual funding before spending time. Never pay an upfront fee.

No API key, paid source, claim/accept action, contact, submission, wallet, payment, or code execution is used. API results may be rate-limited and the hourly job can fail safely; inspect hourly.log.

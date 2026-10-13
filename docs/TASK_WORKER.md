# DAE Task Worker Workbench

The worker turns a reviewed task manifest into real local deliverable files, performs basic safety/quality checks, and packages a submission bundle. It is the first execution step after Task Hunter and the Opportunity Advisor.

## Quick start (Windows CMD)

Create `task.json` using the schema below, then run:

```bat
py -3 scripts\dae_task_worker.py --manifest task.json --output work-output
```

The worker creates `work-output\<task_id>\` and a ZIP bundle next to it. Open `dae_execution_report.json` and inspect every file before submitting it.

## Manifest schema

```json
{
  "task_id": "sample-docs-task",
  "title": "Prepare a short documentation deliverable",
  "source_url": "https://example.com/task-terms",
  "deliverables": [
    {
      "path": "deliverables/summary.md",
      "content": "# Summary\n\nA reviewed draft goes here.\n"
    }
  ]
}
```

## What it actually does

1. Validates the manifest and rejects path traversal.
2. Writes the declared UTF-8 deliverables into an isolated task workspace.
3. Checks for empty files and obvious private-key/API-secret patterns.
4. Records SHA-256 hashes and a machine-readable execution report.
5. Packages all output into a ZIP bundle.

## What it does not do

- It does not discover or accept a task itself; use the hourly scanner and advisor first.
- It does not run arbitrary task-provided shell commands, install dependencies, or execute untrusted repositories.
- It does not create accounts, message clients, submit deliverables, sign transactions, pay fees, or claim revenue.
- `READY_FOR_HUMAN_REVIEW` means only that these local checks passed. It is not proof of correctness, eligibility, acceptance, funding, or payment.

## Recommended earning loop

1. **Hunter:** discover a current task and save its official terms and URL.
2. **Gate:** manually confirm funder, deadline, eligibility, acceptance criteria, and no-upfront-payment requirement.
3. **Worker:** prepare the task manifest and execute this workbench.
4. **QA:** inspect the output, run project-specific tests in a trusted environment, and revise until it meets the acceptance criteria.
5. **Submit:** a human submits through the official platform.
6. **Revenue ledger:** record the submission ID, acceptance evidence, gross payout, fees, net received, time spent, and payment transaction/reference. Count revenue only after receipt is verified.

The worker is intentionally local-first. Automated client contact and submission should be added only with platform-specific adapters, idempotency, explicit permissions, and a human approval gate.

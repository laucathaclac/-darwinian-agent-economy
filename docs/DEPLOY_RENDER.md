# Deploy DAE HealthGuard to Render Free

## What this deployment does

The repository includes a Render Blueprint in `render.yaml`. It creates a free Python web service named `dae-healthguard`, runs the HealthGuard HTTP API, and configures `/health` as the service health check.

The API:
- Serves `GET /health`.
- Serves `GET /.well-known/agent-card.json`.
- Accepts `POST /v1/assess` with a normalized JSON snapshot.
- Does not fetch live lending positions, sign transactions, or hold wallet credentials.

The free instance may spin down when idle, so first requests after inactivity can be delayed. Free-tier availability and current limits are controlled by Render and may change.

## Deploy steps

1. Sign in to Render using the account you want to own the service.
2. Open Render's Blueprint creation flow and connect the public DAE GitHub repository.
3. Select the `feat/healthguard-agent-mvp` branch while this pull request remains unmerged.
4. Review the proposed service `dae-healthguard` and confirm the plan is `Free`.
5. Apply the Blueprint and wait for the first deploy to finish.
6. Open the generated service URL and verify `/health` returns JSON with `"ok": true`.
7. Open `/.well-known/agent-card.json` and verify its `url` matches the generated public service URL.

After PR #17 is merged into `main`, update the Blueprint's `branch` field to `main` in a follow-up change so deployments track the stable branch.

## Security and readiness notes

- Never put seed phrases, private keys, or wallet passwords into Render environment variables.
- No wallet is required for this API-only deployment.
- Do not market the current endpoint as live protocol monitoring: the assessment endpoint evaluates user-supplied normalized data.
- Public hosting does not register an ERC-8004 identity, list the agent on a marketplace, or create qualifying hires/on-chain actions.
- Do not submit hackathon evidence until endpoint responsiveness and all required on-chain criteria are independently verified.

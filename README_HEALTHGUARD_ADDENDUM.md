# HealthGuard quickstart addendum

DAE includes a local, offline HealthGuard assessment core. It is not a live chain-connected agent yet.

From the repository root on Windows:

```bat
py -3 -m unittest discover -s tests -v
py -3 scripts\dae_healthguard.py examples\healthguard_position.json
```

The example JSON is a demo fixture, not live market data. Update observed_at to a current timezone-aware ISO-8601 timestamp before expecting a non-stale assessment.

See docs/HEALTHGUARD.md and docs/DAE_2_HANDOVER.md.

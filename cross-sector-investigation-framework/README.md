# Cross-Sector Investigation Framework

This is a synthetic, non-operational Python reference for evidence-aware intake.
It records provenance, enforces ordered handling states, and stores audit events.
It does not access services, identify people, or determine guilt.

## Run

From this directory:

```text
python -m src.main
python -m unittest discover -s tests
```

The expected demonstration record is `report-001`. Its source reference and
provenance remain unchanged while it moves through preservation, review, and
explicit escalation.

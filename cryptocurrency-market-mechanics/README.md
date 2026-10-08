# Cryptocurrency Marketplace Mechanics

This project models a synthetic marketplace event sequence for defensive analysis. It contains no real identities, services, credentials, or operational access instructions.

## Run

From this directory:

```bash
PYTHONPATH=src python src/main.py
```

Expected output:

```text
order-1001: valid synthetic sequence
```

## Test

```bash
python -m unittest discover -s tests
```

The model records roles, state transitions, and continuity errors. A validation error is an observation about the synthetic sequence; it is not a finding of guilt or intent.

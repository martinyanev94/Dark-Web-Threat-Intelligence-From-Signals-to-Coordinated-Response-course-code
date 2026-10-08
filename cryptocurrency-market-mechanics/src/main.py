from pathlib import Path
from marketplace import analyze, load_events


ROOT = Path(__file__).resolve().parents[1]
events = load_events(str(ROOT / "data" / "events.json"))

for marketplace in ("market-alpha", "market-beta"):
    report = analyze(events, marketplace)
    print(f"{report.marketplace}: indicators={list(report.indicator_ids)}")
    print(f"evidence={list(report.evidence_ids)}")

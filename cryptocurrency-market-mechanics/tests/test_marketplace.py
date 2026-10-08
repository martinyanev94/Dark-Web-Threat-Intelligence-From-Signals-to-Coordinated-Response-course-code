import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from marketplace import analyze, load_events


EVENTS = load_events(str(Path(__file__).parents[1] / "data" / "events.json"))


def test_maintenance_is_not_exit_signal():
    report = analyze(EVENTS, "market-alpha")
    assert "review_shutdown_pattern" not in report.indicator_ids


def test_combined_shutdown_signals_need_review():
    report = analyze(EVENTS, "market-beta")
    assert "review_shutdown_pattern" in report.indicator_ids
    assert "ev-beta-shutdown" in report.evidence_ids


def test_report_is_scoped_to_marketplace():
    report = analyze(EVENTS, "market-alpha")
    assert "ev-beta-shutdown" not in report.evidence_ids

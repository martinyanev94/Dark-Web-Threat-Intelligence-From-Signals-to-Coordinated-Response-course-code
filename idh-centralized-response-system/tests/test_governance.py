from datetime import date

from src.governance import GovernedReport, Role, authorized_view, record_access


def report() -> GovernedReport:
    return GovernedReport(
        "R-204",
        "synthetic-source",
        "observed fact",
        0.72,
        date(2027, 10, 5),
        frozenset({Role.ANALYST, Role.CUSTODIAN}),
        "triage",
    )


def test_analyst_receives_minimized_view() -> None:
    view = authorized_view(report(), Role.ANALYST, "triage")
    assert view is not None
    assert "source_ref" not in view
    assert view["report_id"] == "R-204"


def test_purpose_mismatch_is_denied() -> None:
    assert authorized_view(report(), Role.ANALYST, "investigation") is None


def test_custodian_receives_source_reference() -> None:
    view = authorized_view(report(), Role.CUSTODIAN, "triage")
    assert view is not None
    assert view["source_ref"] == "synthetic-source"


def test_access_decision_is_audited() -> None:
    _, event = record_access(report(), Role.ANALYST, "investigation", date(2026, 10, 5))
    assert event.decision == "denied"
    assert event.report_id == "R-204"

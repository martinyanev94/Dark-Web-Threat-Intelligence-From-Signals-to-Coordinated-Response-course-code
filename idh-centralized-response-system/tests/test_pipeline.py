from src.governance import GovernancePolicy
from src.pipeline import AccessRequest, Report, ResponsePipeline


def make_pipeline() -> ResponsePipeline:
    return ResponsePipeline(
        GovernancePolicy(
            allowed_roles={"specialist": frozenset({"specialist_review"})},
            allowed_fields={"specialist_review": frozenset({"report_id", "category", "confidence", "rationale"})},
        )
    )


def make_report() -> Report:
    return Report(
        "R-204", "exploitation", "synthetic indicator", "medium", ("E-204",), "incomplete", "high", "review required"
    )


def test_authorized_request_gets_minimized_view() -> None:
    result = make_pipeline().process(make_report(), AccessRequest("reviewer-7", "specialist", "specialist_review"))
    assert result.view == {
        "report_id": "R-204",
        "category": "exploitation",
        "confidence": "medium",
        "rationale": "review required",
    }
    assert result.audit[-1].decision == "allow"


def test_unauthorized_purpose_is_denied_without_erasing_report() -> None:
    result = make_pipeline().process(make_report(), AccessRequest("viewer-2", "specialist", "general_distribution"))
    assert result.view == {}
    assert result.audit[-1].decision == "deny"
    assert result.audit[-1].report_id == "R-204"


def test_report_provenance_remains_on_protected_record() -> None:
    report = make_report()
    assert report.provenance == ("E-204",)
    assert report.evidence_status == "incomplete"

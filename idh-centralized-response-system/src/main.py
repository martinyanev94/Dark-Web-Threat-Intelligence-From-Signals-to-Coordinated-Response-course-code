from .governance import GovernancePolicy
from .pipeline import AccessRequest, Report, ResponsePipeline


def build_pipeline() -> ResponsePipeline:
    policy = GovernancePolicy(
        allowed_roles={
            "specialist": frozenset({"specialist_review"}),
            "coordinator": frozenset({"specialist_review", "coordination"}),
        },
        allowed_fields={
            "specialist_review": frozenset({"report_id", "category", "confidence", "rationale"}),
            "coordination": frozenset({"report_id", "category", "confidence", "priority"}),
        },
    )
    return ResponsePipeline(policy)


def demo() -> None:
    pipeline = build_pipeline()
    report = Report(
        report_id="R-204",
        category="exploitation",
        observed_fact="synthetic listing contains a possible exploitation indicator",
        confidence="medium",
        provenance=("E-204",),
        evidence_status="incomplete",
        priority="high",
        rationale="potential harm requires specialist review; corroboration remains open",
    )
    result = pipeline.process(report, AccessRequest("reviewer-7", "specialist", "specialist_review"))
    print(result)


if __name__ == "__main__":
    demo()

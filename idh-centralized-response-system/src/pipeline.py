from dataclasses import dataclass, field
from typing import Any

from .governance import AccessEvent, GovernancePolicy, evaluate_access


@dataclass(frozen=True)
class Report:
    report_id: str
    category: str
    observed_fact: str
    confidence: str
    provenance: tuple[str, ...]
    evidence_status: str
    priority: str
    rationale: str
    retention_days: int = 90


@dataclass(frozen=True)
class AccessRequest:
    requester: str
    role: str
    purpose: str


@dataclass
class PipelineResult:
    report_id: str
    review_lane: str
    view: dict[str, Any]
    audit: list[AccessEvent] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class ResponsePipeline:
    def __init__(self, policy: GovernancePolicy):
        self.policy = policy

    def process(self, report: Report, request: AccessRequest) -> PipelineResult:
        fields, event = evaluate_access(
            report.report_id,
            request.requester,
            request.role,
            request.purpose,
            self.policy,
        )
        lane = "specialist" if report.category in {"exploitation", "trafficking"} else "general"
        values = {
            "report_id": report.report_id,
            "category": report.category,
            "observed_fact": report.observed_fact,
            "confidence": report.confidence,
            "provenance": list(report.provenance),
            "evidence_status": report.evidence_status,
            "priority": report.priority,
            "rationale": report.rationale,
            "retention_days": report.retention_days,
        }
        view = {key: values[key] for key in fields if key in values}
        if event.decision == "deny":
            view = {}
        return PipelineResult(report.report_id, lane, view, [event])

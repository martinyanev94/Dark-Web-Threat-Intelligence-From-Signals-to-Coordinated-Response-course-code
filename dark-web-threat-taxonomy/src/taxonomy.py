from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict


class HarmType(str, Enum):
    ACCESS_ATTEMPT = "access_attempt"
    SERVICE_DISRUPTION = "service_disruption"
    EXPLOITATION_SIGNAL = "exploitation_signal"


class TargetCategory(str, Enum):
    PEOPLE = "people"
    PROPERTY = "property"
    GOVERNMENT = "government"


class Confidence(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class ThreatRecord:
    record_id: str
    observed_fact: str
    harm_type: HarmType
    target: TargetCategory
    urgency: int
    confidence: Confidence
    provenance: str
    review_status: str = "unreviewed"

    def __post_init__(self) -> None:
        if not self.record_id.strip():
            raise ValueError("record_id must not be empty")
        if not self.observed_fact.strip():
            raise ValueError("observed_fact must not be empty")
        if not self.provenance.strip():
            raise ValueError("provenance must not be empty")
        if not 0 <= self.urgency <= 4:
            raise ValueError("urgency must be between 0 and 4")


@dataclass(frozen=True)
class PriorityResult:
    score: int
    band: str
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


HARM_POINTS = {
    HarmType.ACCESS_ATTEMPT: 2,
    HarmType.SERVICE_DISRUPTION: 3,
    HarmType.EXPLOITATION_SIGNAL: 4,
}

TARGET_POINTS = {
    TargetCategory.PEOPLE: 3,
    TargetCategory.PROPERTY: 2,
    TargetCategory.GOVERNMENT: 3,
}

CONFIDENCE_POINTS = {
    Confidence.LOW: 0,
    Confidence.MEDIUM: 2,
    Confidence.HIGH: 3,
}


def calculate_priority(record: ThreatRecord) -> PriorityResult:
    score = (
        HARM_POINTS[record.harm_type]
        + TARGET_POINTS[record.target]
        + record.urgency
        + CONFIDENCE_POINTS[record.confidence]
    )
    band = "urgent review" if score >= 10 else "review" if score >= 5 else "routine"
    rationale = (
        f"harm={HARM_POINTS[record.harm_type]}, "
        f"target={TARGET_POINTS[record.target]}, "
        f"urgency={record.urgency}, "
        f"confidence={CONFIDENCE_POINTS[record.confidence]}"
    )
    return PriorityResult(score=score, band=band, rationale=rationale)

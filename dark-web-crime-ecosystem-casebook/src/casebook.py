from dataclasses import dataclass
from enum import Enum

class Ecosystem(str, Enum):
    HUMAN_TRAFFICKING = "human_trafficking"

class MitigationType(str, Enum):
    PREVENTION = "prevention"
    INVESTIGATION = "investigation"
    VICTIM_SUPPORT = "victim_support"
    DISRUPTION = "disruption"

@dataclass(frozen=True)
class CaseProfile:
    case_id: str
    ecosystem: Ecosystem
    harms: tuple[str, ...]

@dataclass(frozen=True)
class Mitigation:
    mitigation_id: str
    case_id: str
    ecosystem: Ecosystem
    mitigation_type: MitigationType
    stakeholder: str
    action: str
    rationale: str
    confidence: str
    provenance: tuple[str, ...]
    applies_to_harms: tuple[str, ...] = ()

def validate_mitigation(item: Mitigation) -> None:
    if not item.mitigation_id or not item.case_id:
        raise ValueError("identifiers are required")
    if not item.stakeholder.strip():
        raise ValueError("stakeholder is required")
    if not item.action.strip() or not item.rationale.strip():
        raise ValueError("action and rationale are required")
    if item.confidence not in {"low", "medium", "high"}:
        raise ValueError("confidence must be low, medium, or high")
    if not item.provenance:
        raise ValueError("provenance is required")

def build_mitigations(case: CaseProfile) -> list[Mitigation]:
    shared = {"case_id": case.case_id, "ecosystem": case.ecosystem}
    records = [
        Mitigation(f"{case.case_id}-prevention", **shared, mitigation_type=MitigationType.PREVENTION, stakeholder="community and safeguarding partners", action="reduce exposure and strengthen trusted reporting routes", rationale="address enabling conditions before harm escalates", confidence="medium", provenance=("S00034",), applies_to_harms=case.harms),
        Mitigation(f"{case.case_id}-investigation", **shared, mitigation_type=MitigationType.INVESTIGATION, stakeholder="authorized investigative teams", action="preserve and analyze evidence under lawful controls", rationale="evidence handling requires specialized capability", confidence="medium", provenance=("S00034",), applies_to_harms=case.harms),
        Mitigation(f"{case.case_id}-victim-support", **shared, mitigation_type=MitigationType.VICTIM_SUPPORT, stakeholder="safeguarding services", action="provide safety planning and referral", rationale="support addresses affected people directly", confidence="high", provenance=("S00038",), applies_to_harms=case.harms),
        Mitigation(f"{case.case_id}-disruption", **shared, mitigation_type=MitigationType.DISRUPTION, stakeholder="law enforcement and platform partners", action="coordinate lawful intervention against enabling channels", rationale="coordination supports sustained intervention", confidence="medium", provenance=("S00034", "S00036"), applies_to_harms=case.harms),
    ]
    for item in records:
        validate_mitigation(item)
    return records

def group_by_type(items: list[Mitigation]) -> dict[str, list[Mitigation]]:
    grouped: dict[str, list[Mitigation]] = {}
    for item in items:
        validate_mitigation(item)
        grouped.setdefault(item.mitigation_type.value, []).append(item)
    return grouped

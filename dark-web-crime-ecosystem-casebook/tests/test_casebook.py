import pytest
from src.casebook import CaseProfile, Ecosystem, Mitigation, MitigationType, build_mitigations, group_by_type, validate_mitigation

def test_builds_four_response_lanes():
    case = CaseProfile("case-trafficking-01", Ecosystem.HUMAN_TRAFFICKING, ("exploitation",))
    records = build_mitigations(case)
    grouped = group_by_type(records)
    assert len(records) == 4
    assert set(grouped) == {"prevention", "investigation", "victim_support", "disruption"}

def test_empty_stakeholder_is_rejected():
    item = Mitigation("bad", "case-1", Ecosystem.HUMAN_TRAFFICKING, MitigationType.PREVENTION, " ", "act", "reason", "medium", ("S00034",))
    with pytest.raises(ValueError, match="stakeholder"):
        validate_mitigation(item)

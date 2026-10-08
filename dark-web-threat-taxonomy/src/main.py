import json

from taxonomy import (
    Confidence,
    HarmType,
    TargetCategory,
    ThreatRecord,
    calculate_priority,
)


record = ThreatRecord(
    record_id="synthetic-001",
    observed_fact="Repeated access attempts recorded by the service",
    harm_type=HarmType.ACCESS_ATTEMPT,
    target=TargetCategory.PROPERTY,
    urgency=4,
    confidence=Confidence.MEDIUM,
    provenance="synthetic service log summary",
)

result = calculate_priority(record)
print(json.dumps({"record": record.record_id, "priority": result.to_dict()}, indent=2))

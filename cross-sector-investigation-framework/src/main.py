from .workflow import EvidenceStatus, escalate, synthetic_record, transition


def main() -> None:
    record = synthetic_record()
    transition(record, "custodian", EvidenceStatus.PRESERVED, "stored synthetic reference")
    transition(record, "review-analyst", EvidenceStatus.UNDER_REVIEW, "checked required fields")
    escalate(record, "specialist-reviewer", "possible cross-jurisdiction handoff")

    print(f"{record.evidence_id}: {record.status.value}")
    print(f"source={record.provenance.source_label}")
    print(f"audit_events={len(record.audit_log)}")
    print(f"escalation={record.escalation}")


if __name__ == "__main__":
    main()

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class EvidenceStatus(str, Enum):
    RECEIVED = "received"
    PRESERVED = "preserved"
    UNDER_REVIEW = "under_review"
    ESCALATED = "escalated"


@dataclass(frozen=True)
class Provenance:
    source_label: str
    collected_at: str
    collector_role: str


@dataclass(frozen=True)
class AuditEvent:
    actor_role: str
    action: str
    from_status: Optional[EvidenceStatus]
    to_status: EvidenceStatus
    note: str


@dataclass
class EvidenceRecord:
    evidence_id: str
    source_reference: str
    provenance: Provenance
    status: EvidenceStatus = EvidenceStatus.RECEIVED
    escalation: Optional[str] = None
    audit_log: list[AuditEvent] = field(default_factory=list)

    def validate(self) -> None:
        if not self.evidence_id.strip():
            raise ValueError("evidence_id is required")
        if not self.source_reference.strip():
            raise ValueError("source_reference is required")
        if not self.provenance.source_label.strip():
            raise ValueError("provenance source_label is required")
        if not self.provenance.collector_role.strip():
            raise ValueError("provenance collector_role is required")
        if not self.provenance.collected_at.strip():
            raise ValueError("provenance collected_at is required")


ALLOWED_TRANSITIONS = {
    EvidenceStatus.RECEIVED: {EvidenceStatus.PRESERVED},
    EvidenceStatus.PRESERVED: {EvidenceStatus.UNDER_REVIEW},
    EvidenceStatus.UNDER_REVIEW: {EvidenceStatus.ESCALATED},
}


def transition(
    record: EvidenceRecord,
    actor_role: str,
    target: EvidenceStatus,
    note: str,
) -> None:
    record.validate()
    if target not in ALLOWED_TRANSITIONS.get(record.status, set()):
        raise ValueError(f"invalid transition: {record.status} -> {target}")
    if not actor_role.strip() or not note.strip():
        raise ValueError("actor_role and note are required")
    previous = record.status
    record.status = target
    record.audit_log.append(
        AuditEvent(
            actor_role=actor_role,
            action="status_transition",
            from_status=previous,
            to_status=target,
            note=note,
        )
    )


def escalate(record: EvidenceRecord, actor_role: str, reason: str) -> None:
    if record.status is not EvidenceStatus.UNDER_REVIEW:
        raise ValueError("only reviewed evidence can be escalated")
    if not reason.strip():
        raise ValueError("escalation reason is required")
    record.escalation = reason
    transition(record, actor_role, EvidenceStatus.ESCALATED, reason)


def synthetic_record() -> EvidenceRecord:
    return EvidenceRecord(
        evidence_id="report-001",
        source_reference="hash-demo-001",
        provenance=Provenance(
            source_label="public-report-17",
            collected_at="2026-10-05T16:00:00Z",
            collector_role="intake-analyst",
        ),
    )

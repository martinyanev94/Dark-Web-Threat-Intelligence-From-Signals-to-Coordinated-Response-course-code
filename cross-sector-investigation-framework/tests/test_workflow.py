import unittest

from src.workflow import (
    EvidenceStatus,
    EvidenceRecord,
    Provenance,
    escalate,
    synthetic_record,
    transition,
)


class WorkflowTests(unittest.TestCase):
    def test_full_synthetic_path_preserves_provenance(self):
        record = synthetic_record()
        transition(record, "custodian", EvidenceStatus.PRESERVED, "stored reference")
        transition(record, "reviewer", EvidenceStatus.UNDER_REVIEW, "required fields checked")
        escalate(record, "specialist", "jurisdictional handoff")

        self.assertEqual(record.status, EvidenceStatus.ESCALATED)
        self.assertEqual(record.provenance.source_label, "public-report-17")
        self.assertEqual(record.source_reference, "hash-demo-001")
        self.assertEqual(len(record.audit_log), 3)

    def test_escalation_cannot_bypass_review(self):
        record = synthetic_record()
        with self.assertRaises(ValueError):
            escalate(record, "specialist", "unreviewed input")

    def test_missing_source_reference_is_rejected(self):
        record = EvidenceRecord(
            evidence_id="report-002",
            source_reference="",
            provenance=Provenance("synthetic", "2026-10-05T16:00:00Z", "analyst"),
        )
        with self.assertRaises(ValueError):
            record.validate()


if __name__ == "__main__":
    unittest.main()

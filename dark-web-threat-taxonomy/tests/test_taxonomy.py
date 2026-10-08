import sys
from dataclasses import replace
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from taxonomy import (
    Confidence,
    HarmType,
    TargetCategory,
    ThreatRecord,
    calculate_priority,
)


class PriorityTests(unittest.TestCase):
    def setUp(self):
        self.record = ThreatRecord(
            record_id="synthetic-001",
            observed_fact="Repeated access attempts recorded by the service",
            harm_type=HarmType.ACCESS_ATTEMPT,
            target=TargetCategory.PROPERTY,
            urgency=4,
            confidence=Confidence.MEDIUM,
            provenance="synthetic service log summary",
        )

    def test_running_example_is_urgent_review(self):
        result = calculate_priority(self.record)
        self.assertEqual(result.score, 10)
        self.assertEqual(result.band, "urgent review")
        self.assertNotIn("guilt", result.rationale.lower())

    def test_low_confidence_lowers_queue_priority_only(self):
        result = calculate_priority(replace(self.record, confidence=Confidence.LOW))
        self.assertEqual(result.score, 8)
        self.assertEqual(result.band, "review")

    def test_urgency_boundaries_are_validated(self):
        self.assertEqual(calculate_priority(replace(self.record, urgency=0)).score, 6)
        self.assertEqual(calculate_priority(replace(self.record, urgency=4)).score, 10)
        with self.assertRaises(ValueError):
            ThreatRecord(
                record_id="bad",
                observed_fact="synthetic fact",
                harm_type=HarmType.ACCESS_ATTEMPT,
                target=TargetCategory.PROPERTY,
                urgency=5,
                confidence=Confidence.MEDIUM,
                provenance="synthetic source",
            )


if __name__ == "__main__":
    unittest.main()

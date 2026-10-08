import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from comparison import TechnologyClaim, generate_brief


def test_bounded_claim_passes():
    claim = TechnologyClaim("TOR", "routing", "TOR uses multi-hop routing.", ["routing"], "needs corroboration")
    assert generate_brief([claim])["issues"] == []


def test_absolute_claim_is_rejected():
    claim = TechnologyClaim("TOR", "privacy", "TOR guarantees perfect anonymity.", ["routing"], "needs corroboration")
    assert "remove unsupported absolute wording" in generate_brief([claim])["issues"]


def test_missing_evidence_is_rejected():
    claim = TechnologyClaim("Freenet", "storage", "Content is distributed.", [], "needs corroboration")
    assert "add an evidence reference" in generate_brief([claim])["issues"]

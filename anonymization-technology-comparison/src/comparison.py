from dataclasses import dataclass
from typing import List

ABSOLUTE_WORDS = {"perfect", "always", "proves", "guarantees"}

@dataclass(frozen=True)
class TechnologyClaim:
    technology: str
    property: str
    wording: str
    evidence: List[str]
    constraint: str


def review_claim(claim: TechnologyClaim) -> List[str]:
    words = set(claim.wording.lower().replace(".", "").split())
    issues = []
    if words & ABSOLUTE_WORDS:
        issues.append("remove unsupported absolute wording")
    if not claim.evidence:
        issues.append("add an evidence reference")
    if not claim.constraint:
        issues.append("add an investigation constraint")
    return issues


def generate_brief(claims: List[TechnologyClaim]) -> dict:
    rows = []
    issues = []
    for claim in claims:
        claim_issues = review_claim(claim)
        issues.extend(f"{claim.technology}: {issue}" for issue in claim_issues)
        rows.append({
            "technology": claim.technology,
            "property": claim.property,
            "statement": claim.wording,
            "evidence": claim.evidence,
            "investigation_constraint": claim.constraint,
            "review_issues": claim_issues,
        })
    return {"rows": rows, "issues": issues}

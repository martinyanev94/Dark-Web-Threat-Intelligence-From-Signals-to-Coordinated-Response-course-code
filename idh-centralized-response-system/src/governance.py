from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class GovernancePolicy:
    allowed_roles: dict[str, frozenset[str]]
    allowed_fields: dict[str, frozenset[str]]
    retention_days: int = 90


@dataclass(frozen=True)
class AccessEvent:
    report_id: str
    requester: str
    purpose: str
    decision: str
    reason: str
    timestamp: str


def evaluate_access(
    report_id: str,
    requester: str,
    role: str,
    purpose: str,
    policy: GovernancePolicy,
) -> tuple[set[str], AccessEvent]:
    timestamp = datetime.now(timezone.utc).isoformat()
    purposes = policy.allowed_roles.get(role, frozenset())
    fields = policy.allowed_fields.get(purpose, frozenset())
    if purpose not in purposes:
        return set(), AccessEvent(report_id, requester, purpose, "deny", "purpose not allowed for role", timestamp)
    return set(fields), AccessEvent(report_id, requester, purpose, "allow", "minimum fields granted", timestamp)

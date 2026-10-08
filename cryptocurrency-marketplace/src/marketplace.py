from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RiskIndicator:
    kind: str
    severity: str
    explanation: str
    evidence_ids: tuple[str, ...]


def group_feedback_by_vendor(events: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for event in events:
        if event.get("event_type") == "feedback":
            grouped.setdefault(event["vendor_id"], []).append(event)
    for feedback in grouped.values():
        feedback.sort(key=lambda item: item["timestamp"])
    return grouped


def vendor_profile(events: list[dict[str, Any]], vendor_id: str) -> dict[str, Any]:
    for event in events:
        if event.get("event_type") == "vendor_profile" and event.get("vendor_id") == vendor_id:
            return event
    return {"score": 0.0}


def detect_reputation_inconsistency(events: list[dict[str, Any]]) -> list[RiskIndicator]:
    findings: list[RiskIndicator] = []
    by_vendor = group_feedback_by_vendor(events)
    for vendor_id, feedback in by_vendor.items():
        recent = feedback[-3:]
        negatives = [item for item in recent if item["rating"] <= 2]
        profile = vendor_profile(events, vendor_id)
        if len(recent) >= 2 and profile.get("score", 0.0) >= 4.5 and len(negatives) / len(recent) >= 0.5:
            findings.append(RiskIndicator("reputation_inconsistency", "medium", f"{vendor_id} has a high displayed score but frequent recent negative feedback", tuple(item["event_id"] for item in recent)))
    return findings


def detect_escrow_anomalies(events: list[dict[str, Any]]) -> list[RiskIndicator]:
    confirmed: set[str] = set()
    findings: list[RiskIndicator] = []
    for event in events:
        event_type = event.get("event_type")
        if event_type == "receipt_confirmed":
            confirmed.add(event["order_id"])
        elif event_type == "escrow_released" and event["order_id"] not in confirmed:
            findings.append(RiskIndicator("escrow_release_without_confirmation", "high", "Escrow was released before a receipt confirmation was observed", (event["event_id"],)))
    return findings


def detect_shutdown_patterns(events: list[dict[str, Any]]) -> list[RiskIndicator]:
    by_market: dict[str, list[dict[str, Any]]] = {}
    for event in events:
        by_market.setdefault(event["market_id"], []).append(event)
    findings: list[RiskIndicator] = []
    for market_id, items in by_market.items():
        timeline = sorted(items, key=lambda item: item["timestamp"])
        held: list[dict[str, Any]] = []
        for event in timeline:
            if event.get("event_type") == "escrow_held":
                held.append(event)
            elif event.get("event_type") == "market_shutdown":
                later_online = any(item.get("event_type") == "market_online" and item["timestamp"] > event["timestamp"] for item in timeline)
                if held and not later_online:
                    evidence = tuple(item["event_id"] for item in held) + (event["event_id"],)
                    findings.append(RiskIndicator("abrupt_shutdown_pattern", "high", f"{market_id} recorded held escrow before shutdown without a later online event", evidence))
    return findings


def analyze_events(events: list[dict[str, Any]]) -> list[RiskIndicator]:
    findings: list[RiskIndicator] = []
    findings.extend(detect_reputation_inconsistency(events))
    findings.extend(detect_escrow_anomalies(events))
    findings.extend(detect_shutdown_patterns(events))
    return findings

from dataclasses import dataclass
from typing import Iterable
import json


@dataclass(frozen=True)
class Event:
    event_id: str
    marketplace: str
    actor: str
    event_type: str


@dataclass(frozen=True)
class RiskReport:
    marketplace: str
    indicator_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]


def load_events(path: str) -> list[Event]:
    with open(path, encoding="utf-8") as handle:
        raw_events = json.load(handle)
    return [Event(**item) for item in raw_events]


def detect_reputation_inconsistency(events: list[Event]) -> tuple[str | None, list[str]]:
    positive = [e for e in events if e.event_type == "positive_feedback"]
    negative = [e for e in events if e.event_type == "negative_feedback"]
    if len(negative) >= 2 and len(positive) >= 2:
        return "reputation_inconsistency", [e.event_id for e in positive + negative]
    return None, []


def detect_escrow_anomaly(events: list[Event]) -> tuple[str | None, list[str]]:
    held = any(e.event_type == "escrow_held" for e in events)
    released = any(e.event_type == "escrow_released" for e in events)
    confirmed = any(e.event_type == "delivery_confirmed" for e in events)
    if released and not confirmed:
        evidence = [e.event_id for e in events if e.event_type in {"escrow_released", "delivery_confirmed"}]
        return "escrow_anomaly", evidence
    if held and any(e.event_type == "delivery_failed" for e in events):
        evidence = [e.event_id for e in events if e.event_type in {"escrow_held", "delivery_failed"}]
        return "escrow_anomaly", evidence
    return None, []


def detect_shutdown_pattern(events: list[Event]) -> tuple[str | None, list[str]]:
    shutdown = [e for e in events if e.event_type == "market_shutdown"]
    held = [e for e in events if e.event_type == "escrow_held"]
    failed = [e for e in events if e.event_type == "delivery_failed"]
    if shutdown and held and len(failed) >= 2:
        evidence = [e.event_id for e in shutdown + held + failed]
        return "review_shutdown_pattern", evidence
    return None, []


def analyze(events: Iterable[Event], marketplace: str) -> RiskReport:
    scoped = [event for event in events if event.marketplace == marketplace]
    detectors = (detect_reputation_inconsistency, detect_escrow_anomaly, detect_shutdown_pattern)
    indicators: list[str] = []
    evidence: list[str] = []
    for detector in detectors:
        indicator, detector_evidence = detector(scoped)
        if indicator:
            indicators.append(indicator)
            evidence.extend(detector_evidence)
    return RiskReport(marketplace, tuple(indicators), tuple(dict.fromkeys(evidence)))

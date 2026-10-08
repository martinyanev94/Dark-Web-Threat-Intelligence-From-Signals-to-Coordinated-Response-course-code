from dataclasses import dataclass


@dataclass(frozen=True)
class SystemCharter:
    problem: str
    goal: str
    actors: tuple[str, ...]
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    constraints: tuple[str, ...]
    non_goals: tuple[str, ...]


def validate_charter(charter: SystemCharter) -> list[str]:
    errors: list[str] = []
    for field_name in ("problem", "goal"):
        if not getattr(charter, field_name).strip():
            errors.append(f"{field_name} is required")
    for field_name in ("actors", "inputs", "outputs", "constraints", "non_goals"):
        if not getattr(charter, field_name):
            errors.append(f"{field_name} must not be empty")
    if not any("adjud" in item.lower() for item in charter.non_goals):
        errors.append("adjudication boundary must be explicit")
    return errors

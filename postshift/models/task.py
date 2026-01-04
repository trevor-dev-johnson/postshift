from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Task:
    id: str
    title: str
    duration_hours: float
    earliest_start: datetime | None = None
    latest_end: datetime | None = None
    required_energy: float = 0.0
    tags: set[str] = field(default_factory=set)

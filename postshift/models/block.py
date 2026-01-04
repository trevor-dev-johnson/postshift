from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class BlockKind(str, Enum):
    WORK = "work"
    SLEEP = "sleep"
    RECOVERY = "recovery"


@dataclass(frozen=True)
class TimeBlock:
    start: datetime
    end: datetime
    kind: BlockKind
    intensity: float = 1.0

    @property
    def duration_hours(self) -> float:
        seconds = (self.end - self.start).total_seconds()
        return max(0.0, seconds / 3600.0)

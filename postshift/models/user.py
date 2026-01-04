from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UserProfile:
    timezone: str = "UTC"
    energy_max: float = 100.0
    decay_per_hour: float = 5.0

from dataclasses import dataclass

from postshift.core.energy import calculate_energy, EnergyLevel
from postshift.storage.local import EventStore


@dataclass
class AssessmentResult:
    energy: EnergyLevel
    warning: str | None = None


def assess_energy(
    *,
    hours_slept: float,
    night_shift: bool,
    hours_since_shift_end: float,
    consecutive_shifts: int,
) -> AssessmentResult:

    energy = calculate_energy(
        hours_slept=hours_slept,
        night_shift=night_shift,
        hours_since_shift_end=hours_since_shift_end,
        consecutive_shifts=consecutive_shifts,
    )

    warning = None
    if energy == "dead":
        warning = "Recovery strongly recommended. Avoid optional effort."
    elif energy == "low":
        warning = "Low energy. Stick to light tasks and recovery."

    store = EventStore()
    store.log_event(
        event_type="energy_assessed",
        payload={
            "hours_slept": hours_slept,
            "night_shift": night_shift,
            "hours_since_shift_end": hours_since_shift_end,
            "consecutive_shifts": consecutive_shifts,
            "energy": energy,
            "warning": warning,
        },
    )

    return AssessmentResult(energy=energy, warning=warning)

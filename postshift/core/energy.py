from typing import Literal

EnergyLevel = Literal["dead", "low", "normal", "sharp"]

ENERGY_ORDER = ["dead", "low", "normal", "sharp"]

def downgrade(energy: EnergyLevel, steps: int) -> EnergyLevel:
  
  idx = ENERGY_ORDER.index(energy)
  return ENERGY_ORDER[max(0, idx - steps)]

def calculate_energy(
  hours_slept: float,
  night_shift: bool,
  hours_since_shift_end: float,
  consecutive_shifts: int,
) -> EnergyLevel:
  
    if hours_slept < 5:
        energy: EnergyLevel = "dead"
    elif hours_slept < 6.5:
        energy = "low"
    elif hours_slept < 7.5:
        energy = "normal"
    else:
        energy = "sharp"

    if night_shift:
        if hours_since_shift_end < 6:
            energy = downgrade(energy, 2)
        elif hours_since_shift_end < 10:
            energy = downgrade(energy, 1)

    if consecutive_shifts == 2:
        energy = downgrade(energy, 1)
    elif consecutive_shifts >= 3:
        energy = downgrade(energy, 2)

    return energy
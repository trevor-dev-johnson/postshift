from __future__ import annotations

from postshift.core.energy import EnergyConfig, EnergyEngine
from postshift.core.rules import penalty_for_blocks
from postshift.models.block import TimeBlock
from postshift.models.user import UserProfile


def assess(user: UserProfile, blocks: list[TimeBlock], start_energy: float | None = None) -> dict[str, float]:
    config = EnergyConfig(
        energy_max=user.energy_max,
        decay_per_hour=user.decay_per_hour,
    )
    engine = EnergyEngine(config)
    energy0 = user.energy_max if start_energy is None else start_energy
    energy_end = engine.energy_after_blocks(energy0, blocks)
    penalty = penalty_for_blocks(blocks)
    return {"energy_end": float(energy_end), "penalty": float(penalty)}

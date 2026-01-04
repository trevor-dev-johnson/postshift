from datetime import datetime, timedelta
import unittest

from postshift.core.energy import EnergyEngine
from postshift.models.block import BlockKind, TimeBlock


class TestEnergyEngine(unittest.TestCase):
    def test_work_reduces_energy(self) -> None:
        start = datetime(2026, 1, 1, 9, 0, 0)
        end = start + timedelta(hours=2)
        blocks = [TimeBlock(start=start, end=end, kind=BlockKind.WORK)]
        engine = EnergyEngine()
        energy_end = engine.energy_after_blocks(100.0, blocks)
        self.assertLess(energy_end, 100.0)

    def test_sleep_increases_energy(self) -> None:
        start = datetime(2026, 1, 1, 0, 0, 0)
        end = start + timedelta(hours=2)
        blocks = [TimeBlock(start=start, end=end, kind=BlockKind.SLEEP)]
        engine = EnergyEngine()
        energy_end = engine.energy_after_blocks(50.0, blocks)
        self.assertGreater(energy_end, 50.0)


if __name__ == "__main__":
    unittest.main()

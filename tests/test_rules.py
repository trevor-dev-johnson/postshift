from datetime import datetime, timedelta
import unittest

from postshift.core.rules import penalty_for_blocks
from postshift.models.block import BlockKind, TimeBlock


class TestRules(unittest.TestCase):
    def test_penalty_is_float(self) -> None:
        start = datetime(2026, 1, 1, 9, 0, 0)
        end = start + timedelta(hours=1)
        blocks = [TimeBlock(start=start, end=end, kind=BlockKind.WORK)]
        value = penalty_for_blocks(blocks)
        self.assertIsInstance(value, float)


if __name__ == "__main__":
    unittest.main()

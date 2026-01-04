from __future__ import annotations

from postshift.models.block import TimeBlock
from postshift.models.task import Task


def match_tasks_to_windows(tasks: list[Task], windows: list[TimeBlock]) -> dict[str, str]:
    return {}

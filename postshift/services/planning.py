from __future__ import annotations

from postshift.models.block import TimeBlock
from postshift.models.task import Task
from postshift.models.user import UserProfile


def plan(user: UserProfile, tasks: list[Task], windows: list[TimeBlock]) -> dict[str, str]:
    return {}

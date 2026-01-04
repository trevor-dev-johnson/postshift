from __future__ import annotations

from postshift.models.task import Task


def is_task_feasible(task: Task, available_energy: float) -> bool:
    return available_energy >= float(task.required_energy)

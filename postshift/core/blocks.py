from __future__ import annotations

from postshift.models.block import BlockKind, TimeBlock


def is_rest_block(block: TimeBlock) -> bool:
    return block.kind in {BlockKind.SLEEP, BlockKind.RECOVERY}


def is_work_block(block: TimeBlock) -> bool:
    return block.kind == BlockKind.WORK

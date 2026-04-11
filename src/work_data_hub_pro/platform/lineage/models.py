from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LineageLink:
    record_id: str
    parent_record_ids: list[str]
    origin_row_nos: list[int]
    anchor_row_no: int

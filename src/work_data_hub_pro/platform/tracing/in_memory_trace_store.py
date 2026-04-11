from __future__ import annotations

from work_data_hub_pro.platform.contracts.models import FieldTraceEvent


class InMemoryTraceStore:
    def __init__(self) -> None:
        self._events: list[FieldTraceEvent] = []

    def record(self, event: FieldTraceEvent) -> None:
        self._events.append(event)

    def find(self, *, batch_id: str, anchor_row_no: int) -> list[FieldTraceEvent]:
        matches = [
            event
            for event in self._events
            if event.batch_id == batch_id and event.anchor_row_no == anchor_row_no
        ]
        return sorted(matches, key=lambda item: item.event_seq)

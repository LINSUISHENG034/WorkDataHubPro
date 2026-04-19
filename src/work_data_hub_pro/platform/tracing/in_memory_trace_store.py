from __future__ import annotations

from work_data_hub_pro.platform.contracts.models import FieldTraceEvent


class InMemoryTraceStore:
    def __init__(self) -> None:
        self._events: list[FieldTraceEvent] = []
        self._events_by_anchor: dict[tuple[str, int], list[FieldTraceEvent]] | None = None
        self._indexed_event_count = 0

    def record(self, event: FieldTraceEvent) -> None:
        self._events.append(event)

    def find(self, *, batch_id: str, anchor_row_no: int) -> list[FieldTraceEvent]:
        if (
            self._events_by_anchor is None
            or self._indexed_event_count != len(self._events)
        ):
            events_by_anchor: dict[tuple[str, int], list[FieldTraceEvent]] = {}
            for event in self._events:
                key = (event.batch_id, event.anchor_row_no)
                events_by_anchor.setdefault(key, []).append(event)
            for matches in events_by_anchor.values():
                matches.sort(key=lambda item: item.event_seq)
            self._events_by_anchor = events_by_anchor
            self._indexed_event_count = len(self._events)

        matches = self._events_by_anchor.get((batch_id, anchor_row_no), [])
        return list(matches)

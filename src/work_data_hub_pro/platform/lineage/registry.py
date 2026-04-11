from __future__ import annotations

from work_data_hub_pro.platform.lineage.models import LineageLink


class LineageRegistry:
    def __init__(self) -> None:
        self._links: dict[str, LineageLink] = {}

    def register(self, link: LineageLink) -> None:
        self._links[link.record_id] = link

    def get(self, record_id: str) -> LineageLink | None:
        return self._links.get(record_id)

    def all(self) -> list[LineageLink]:
        return list(self._links.values())

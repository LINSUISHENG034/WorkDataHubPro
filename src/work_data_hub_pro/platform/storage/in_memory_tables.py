from __future__ import annotations

from copy import deepcopy


class InMemoryTableStore:
    def __init__(self, seed: dict[str, list[dict[str, object]]] | None = None) -> None:
        self._tables = deepcopy(seed or {})

    def refresh(self, target_name: str, rows: list[dict[str, object]]) -> int:
        self._tables[target_name] = deepcopy(rows)
        return len(rows)

    def upsert(
        self,
        target_name: str,
        rows: list[dict[str, object]],
        *,
        key_fields: list[str],
    ) -> int:
        existing = {
            tuple(row[key] for key in key_fields): row
            for row in self._tables.get(target_name, [])
        }
        for row in rows:
            existing[tuple(row[key] for key in key_fields)] = deepcopy(row)
        self._tables[target_name] = list(existing.values())
        return len(rows)

    def append(self, target_name: str, rows: list[dict[str, object]]) -> int:
        current = self._tables.setdefault(target_name, [])
        current.extend(deepcopy(rows))
        return len(rows)

    def read(self, target_name: str) -> list[dict[str, object]]:
        return deepcopy(self._tables.get(target_name, []))

from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


def _tokens(text: str) -> list[str]:
    return [word.strip(".,!?;:()[]").lower() for word in text.split() if word.strip()]


def _cosine_similarity(left: str, right: str) -> float:
    """Small dependency-free similarity function used for local semantic recall."""
    left_counts = Counter(_tokens(left))
    right_counts = Counter(_tokens(right))
    if not left_counts or not right_counts:
        return 0.0

    shared = set(left_counts) & set(right_counts)
    numerator = sum(left_counts[word] * right_counts[word] for word in shared)
    left_norm = math.sqrt(sum(value * value for value in left_counts.values()))
    right_norm = math.sqrt(sum(value * value for value in right_counts.values()))
    return numerator / (left_norm * right_norm)


@dataclass
class MemoryRecord:
    session_id: str
    user_message: str
    agent_summary: str
    facts: list[str] = field(default_factory=list)


class JsonMemoryStore:
    """Session memory store with the same shape a Redis store would expose."""

    def __init__(self, path: str | Path = ".agent_memory.json") -> None:
        self.path = Path(path)

    def _read_all(self) -> list[dict]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write_all(self, rows: list[dict]) -> None:
        self.path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    def save(self, record: MemoryRecord) -> None:
        rows = self._read_all()
        rows.append({"session_id": record.session_id, "user_message": record.user_message, "agent_summary": record.agent_summary, "facts": record.facts})
        self._write_all(rows)

    def load_session(self, session_id: str) -> list[MemoryRecord]:
        return [MemoryRecord(**row) for row in self._read_all() if row["session_id"] == session_id]

    def search(self, session_id: str, query: str, limit: int = 3) -> list[MemoryRecord]:
        scored = [
            (_cosine_similarity(query, f"{record.user_message} {record.agent_summary}"), record)
            for record in self.load_session(session_id)
        ]
        return [record for score, record in sorted(scored, reverse=True, key=lambda item: item[0])[:limit] if score > 0]

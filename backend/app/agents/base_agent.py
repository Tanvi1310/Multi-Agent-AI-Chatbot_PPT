from __future__ import annotations

from typing import Any


class BaseAgent:
    def __init__(self, name: str, role: str) -> None:
        self.name = name
        self.role = role

    def run(self, **kwargs: Any) -> dict[str, Any]:
        return {"agent": self.name, "role": self.role, "status": "completed", "data": kwargs}

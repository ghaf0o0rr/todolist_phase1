from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Dict, Optional

class Status(str, Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    status: Status = Status.TODO
    deadline: Optional[date] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Project:
    id: int
    name: str
    description: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    tasks: Dict[int, Task] = field(default_factory=dict)
    _next_task_id: int = 0

    def add_task(self, task: Task) -> None:
        self.tasks[task.id] = task

    def next_task_id(self) -> int:
        self._next_task_id += 1
        return self._next_task_id

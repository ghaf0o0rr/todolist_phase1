from __future__ import annotations
import os
from typing import Optional, List
from dotenv import load_dotenv
from .models import Status, Project, Task
from .repository import InMemoryRepository
from .validators import (
    validate_name, validate_description, validate_status, parse_deadline
)
from .errors import LimitExceededError

load_dotenv()

MAX_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECT", "999999"))
MAX_TASKS = int(os.getenv("MAX_NUMBER_OF_TASK", "999999"))

class ToDoService:
    def __init__(self, repo: InMemoryRepository | None = None) -> None:
        self.repo = repo or InMemoryRepository()

    # ---- Projects ----
    def create_project(self, name: str, description: str) -> Project:
        validate_name(name)
        validate_description(description)
        if len(self.repo.list_projects()) >= MAX_PROJECTS:
            raise LimitExceededError("Reached MAX_NUMBER_OF_PROJECT.")
        return self.repo.create_project(name=name.strip(), description=(description or "").strip())

    def edit_project(self, project_id: int, name: Optional[str], description: Optional[str]) -> Project:
        if name is not None:
            validate_name(name)
        if description is not None:
            validate_description(description)
        return self.repo.update_project(project_id, name=name.strip() if name else None,
                                        description=description.strip() if description else None)

    def delete_project(self, project_id: int) -> None:
        # Cascade delete handled in repository delete_project
        self.repo.delete_project(project_id)

    def list_projects(self) -> List[Project]:
        return self.repo.list_projects()

    # ---- Tasks ----
    def create_task(self, project_id: int, title: str, description: str, status: str = "todo", deadline: Optional[str] = None) -> Task:
        validate_name(title)
        validate_description(description)
        validate_status(status)
        deadline_date = parse_deadline(deadline)
        # enforce per-project tasks ceiling across project
        tasks_count = len(self.repo.list_tasks(project_id))
        if tasks_count >= MAX_TASKS:
            raise LimitExceededError("Reached MAX_NUMBER_OF_TASK for this project.")
        return self.repo.create_task(project_id=project_id,
                                     title=title.strip(),
                                     description=(description or "").strip(),
                                     status=Status(status),
                                     deadline=deadline_date)

    def edit_task(self, project_id: int, task_id: int, title: Optional[str] = None, description: Optional[str] = None,
                  status: Optional[str] = None, deadline: Optional[str] = None) -> Task:
        if title is not None:
            validate_name(title)
        if description is not None:
            validate_description(description)
        status_enum = None
        if status is not None:
            validate_status(status)
            status_enum = Status(status)
        deadline_date = None if deadline is None else parse_deadline(deadline)
        return self.repo.update_task(project_id, task_id, title=title, description=description,
                                     status=status_enum, deadline=deadline_date)

    def change_task_status(self, project_id: int, task_id: int, status: str) -> Task:
        validate_status(status)
        return self.repo.update_task(project_id, task_id, status=Status(status))

    def delete_task(self, project_id: int, task_id: int) -> None:
        self.repo.delete_task(project_id, task_id)

    def list_tasks(self, project_id: int):
        return self.repo.list_tasks(project_id)

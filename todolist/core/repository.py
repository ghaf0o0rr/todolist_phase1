from __future__ import annotations
from dataclasses import replace
from typing import Dict, List, Optional
from .models import Project, Task, Status
from .errors import NotFoundError, DuplicateNameError

class InMemoryRepository:
    def __init__(self) -> None:
        self._projects: Dict[int, Project] = {}
        self._next_project_id: int = 0

    # ---- Project ops ----
    def create_project(self, name: str, description: str) -> Project:
        if any(p.name == name for p in self._projects.values()):
            raise DuplicateNameError("Project name must be unique.")
        self._next_project_id += 1
        project = Project(id=self._next_project_id, name=name, description=description)
        self._projects[project.id] = project
        return project

    def update_project(self, project_id: int, name: Optional[str], description: Optional[str]) -> Project:
        p = self.get_project(project_id)
        if name is not None and name != p.name:
            if any(other.name == name for other in self._projects.values() if other.id != project_id):
                raise DuplicateNameError("Project name must be unique.")
            p.name = name
        if description is not None:
            p.description = description
        return p

    def delete_project(self, project_id: int) -> None:
        # Cascade delete: removing the project will also remove its tasks
        if project_id not in self._projects:
            raise NotFoundError("Project not found.")
        del self._projects[project_id]

    def list_projects(self) -> List[Project]:
        return sorted(self._projects.values(), key=lambda p: p.created_at)

    def get_project(self, project_id: int) -> Project:
        try:
            return self._projects[project_id]
        except KeyError:
            raise NotFoundError("Project not found.")

    # ---- Task ops (scoped by project) ----
    def create_task(self, project_id: int, title: str, description: str, status: Status, deadline) -> Task:
        p = self.get_project(project_id)
        task_id = p.next_task_id()
        task = Task(id=task_id, title=title, description=description, status=status, deadline=deadline)
        p.add_task(task)
        return task

    def update_task(self, project_id: int, task_id: int, title=None, description=None, status=None, deadline=None) -> Task:
        p = self.get_project(project_id)
        if task_id not in p.tasks:
            raise NotFoundError("Task not found.")
        t = p.tasks[task_id]
        if title is not None:
            t.title = title
        if description is not None:
            t.description = description
        if status is not None:
            t.status = status
        if deadline is not None:
            t.deadline = deadline
        return t

    def delete_task(self, project_id: int, task_id: int) -> None:
        p = self.get_project(project_id)
        if task_id not in p.tasks:
            raise NotFoundError("Task not found.")
        del p.tasks[task_id]

    def list_tasks(self, project_id: int):
        p = self.get_project(project_id)
        return sorted(p.tasks.values(), key=lambda t: t.created_at)

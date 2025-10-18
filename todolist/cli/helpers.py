from __future__ import annotations
from typing import Iterable
from datetime import date
from ..core.models import Project, Task

def print_projects_table(projects: Iterable[Project]) -> None:
    print(f"{'ID':<4} {'Name':<32} {'Created':<20} Description")
    print("-" * 90)
    for p in projects:
        created = p.created_at.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{p.id:<4} {p.name:<32} {created:<20} {p.description}")

def print_tasks_table(tasks: Iterable[Task]) -> None:
    print(f"{'ID':<4} {'Title':<32} {'Status':<8} {'Deadline':<12} {'Created':<20} Description")
    print("-" * 120)
    for t in tasks:
        deadline = t.deadline.strftime("%Y-%m-%d") if t.deadline else "-"
        created = t.created_at.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{t.id:<4} {t.title:<32} {t.status.value:<8} {deadline:<12} {created:<20} {t.description}")

# (Kept simple to avoid external formatting libs; good enough for Phase 1.)

from __future__ import annotations
import argparse
from typing import Any
from .helpers import print_projects_table, print_tasks_table
from ..core.services import ToDoService
from ..core.errors import ValidationError, DuplicateNameError, NotFoundError, LimitExceededError

service = ToDoService()

def _ok(msg: str) -> None:
    print(f"[OK] {msg}")

def _err(msg: str) -> None:
    print(f"[ERROR] {msg}")

def cmd_projects(args: argparse.Namespace) -> None:
    if args.subcommand == "add":
        try:
            p = service.create_project(name=args.name, description=args.description or "")
            _ok(f"Project created: id={p.id}, name='{p.name}'")
        except (ValidationError, DuplicateNameError, LimitExceededError) as e:
            _err(str(e))

    elif args.subcommand == "edit":
        try:
            p = service.edit_project(project_id=args.id, name=args.name, description=args.description)
            _ok(f"Project updated: id={p.id}, name='{p.name}'")
        except (ValidationError, DuplicateNameError, NotFoundError) as e:
            _err(str(e))

    elif args.subcommand == "delete":
        try:
            service.delete_project(project_id=args.id)
            _ok("Project deleted (cascade tasks removed).")
        except NotFoundError as e:
            _err(str(e))

    elif args.subcommand == "list":
        projects = service.list_projects()
        if not projects:
            print("No projects yet.")
        else:
            print_projects_table(projects)

def cmd_tasks(args: argparse.Namespace) -> None:
    if args.subcommand == "add":
        try:
            t = service.create_task(project_id=args.project_id, title=args.title,
                                    description=args.description or "", status=args.status, deadline=args.deadline)
            _ok(f"Task created: id={t.id} in project {args.project_id}")
        except (ValidationError, LimitExceededError, NotFoundError) as e:
            _err(str(e))

    elif args.subcommand == "edit":
        try:
            t = service.edit_task(project_id=args.project_id, task_id=args.task_id, title=args.title,
                                  description=args.description, status=args.status, deadline=args.deadline)
            _ok(f"Task updated: id={t.id} in project {args.project_id}")
        except (ValidationError, NotFoundError) as e:
            _err(str(e))

    elif args.subcommand == "status":
        try:
            t = service.change_task_status(project_id=args.project_id, task_id=args.task_id, status=args.status)
            _ok(f"Task status changed: id={t.id} -> {t.status.value}")
        except (ValidationError, NotFoundError) as e:
            _err(str(e))

    elif args.subcommand == "delete":
        try:
            service.delete_task(project_id=args.project_id, task_id=args.task_id)
            _ok("Task deleted.")
        except NotFoundError as e:
            _err(str(e))

    elif args.subcommand == "list":
        try:
            tasks = service.list_tasks(project_id=args.project_id)
            if not tasks:
                print("No tasks in this project.")
            else:
                print_tasks_table(tasks)
        except NotFoundError as e:
            _err(str(e))

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todolist", description="ToDoList CLI (Phase 1 - In-Memory)")
    sub = parser.add_subparsers(dest="command")

    # --- projects ---
    p = sub.add_parser("projects", help="Project commands")
    p_sub = p.add_subparsers(dest="subcommand")

    p_add = p_sub.add_parser("add", help="Add a project")
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--description", default="")
    p_add.set_defaults(func=cmd_projects)

    p_edit = p_sub.add_parser("edit", help="Edit a project")
    p_edit.add_argument("--id", type=int, required=True)
    p_edit.add_argument("--name")
    p_edit.add_argument("--description")
    p_edit.set_defaults(func=cmd_projects)

    p_del = p_sub.add_parser("delete", help="Delete a project (cascade deletes tasks)")
    p_del.add_argument("--id", type=int, required=True)
    p_del.set_defaults(func=cmd_projects)

    p_list = p_sub.add_parser("list", help="List projects")
    p_list.set_defaults(func=cmd_projects)

    # --- tasks ---
    t = sub.add_parser("tasks", help="Task commands (scoped by project)")
    t_sub = t.add_subparsers(dest="subcommand")

    t_add = t_sub.add_parser("add", help="Add a task to a project")
    t_add.add_argument("--project-id", type=int, required=True)
    t_add.add_argument("--title", required=True)
    t_add.add_argument("--description", default="")
    t_add.add_argument("--status", default="todo", choices=["todo", "doing", "done"])
    t_add.add_argument("--deadline", help="YYYY-MM-DD")
    t_add.set_defaults(func=cmd_tasks)

    t_edit = t_sub.add_parser("edit", help="Edit a task")
    t_edit.add_argument("--project-id", type=int, required=True)
    t_edit.add_argument("--task-id", type=int, required=True)
    t_edit.add_argument("--title")
    t_edit.add_argument("--description")
    t_edit.add_argument("--status", choices=["todo", "doing", "done"])
    t_edit.add_argument("--deadline", help="YYYY-MM-DD")
    t_edit.set_defaults(func=cmd_tasks)

    t_status = t_sub.add_parser("status", help="Change a task's status")
    t_status.add_argument("--project-id", type=int, required=True)
    t_status.add_argument("--task-id", type=int, required=True)
    t_status.add_argument("--status", required=True, choices=["todo", "doing", "done"])
    t_status.set_defaults(func=cmd_tasks)

    t_del = t_sub.add_parser("delete", help="Delete a task")
    t_del.add_argument("--project-id", type=int, required=True)
    t_del.add_argument("--task-id", type=int, required=True)
    t_del.set_defaults(func=cmd_tasks)

    t_list = t_sub.add_parser("list", help="List all tasks in a project")
    t_list.add_argument("--project-id", type=int, required=True)
    t_list.set_defaults(func=cmd_tasks)

    return parser

def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return
    args.func(args)

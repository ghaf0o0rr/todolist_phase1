# ToDoList – Python OOP (In-Memory) – Phase 1

A simple, layered ToDoList CLI app that keeps data **in memory** (no persistence yet), following the
Phase 1 requirements. It uses:
- Python OOP with a **core/business** layer separate from the **CLI** layer
- **.env** limits for MAX_NUMBER_OF_PROJECT and MAX_NUMBER_OF_TASK
- **argparse** CLI (no third-party CLI deps)
- Poetry for dependency management (optional but recommended)

## Quick Start

```bash
# 0) (Optional) Use Poetry
poetry install
cp .env.example .env

# 1) Run help
poetry run python main.py --help

# 2) Add a project
poetry run python main.py projects add --name "My Project" --description "Short description"

# 3) List projects
poetry run python main.py projects list

# 4) Add a task into project id 1
poetry run python main.py tasks add --project-id 1 --title "Write report" --status todo --deadline 2025-12-31

# 5) List all tasks in project id 1
poetry run python main.py tasks list --project-id 1

# 6) Change a task's status
poetry run python main.py tasks status --project-id 1 --task-id 1 --status done
```

## Notes
- Valid statuses: `todo`, `doing`, `done`
- Name/title length ≤ 30 chars; description ≤ 150 chars
- Deleting a project **cascade deletes** its tasks
- Data is lost each time the app stops — persistence will be added in later phases

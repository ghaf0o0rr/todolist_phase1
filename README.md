```markdown
# ToDoList — Python OOP (In-Memory) — Phase 1

A small, layered **ToDoList CLI** that stores data **in memory** (no persistence yet).  
Phase-1 focuses on clean OOP design, validation, and a simple CLI — ready to plug in persistence in later phases.

---

## ✨ Features (Phase-1)

- **Layered OOP**: core/business logic isolated from the CLI layer.
- **Projects & Tasks**: create, edit, delete, list; change task status.
- **Validation**
  - Status: `todo`, `doing`, `done`
  - Title ≤ **30** chars; description ≤ **150** chars
  - Deadline format: **YYYY-MM-DD**
- **Cascade delete**: deleting a project removes all its tasks.
- **Config via `.env`**
  - `MAX_NUMBER_OF_PROJECT`
  - `MAX_NUMBER_OF_TASK`
- **Argparse CLI** (no third-party CLI deps).
- **Tests**: minimal `pytest` smoke test.
- **Poetry** config included (optional).

---

## 🧱 Project Structure

```

todolist_phase1/
main.py
README.md
pyproject.toml
.env.example
repl.py                  # optional helper for single-process testing
todolist/
**init**.py
core/
**init**.py
models.py            # Project, Task, Status (Enum)
validators.py        # length, status, deadline parsing
repository.py        # in-memory repo (+ cascade delete)
services.py          # business rules + .env limits
errors.py            # typed exceptions
cli/
**init**.py
app.py               # argparse commands
helpers.py           # simple tabular output
tests/
test_basic.py          # tiny smoke test

````

---

## 🧰 Requirements

- Python **3.10+**
- Optional: **Poetry**
- Dev/test deps: `python-dotenv`, `pytest`

---

## 🚀 Setup

### Option A — Poetry
```bash
poetry install
cp .env.example .env
````

### Option B — venv + pip

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install python-dotenv pytest
cp .env.example .env
```

### `.env` values

```env
MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=100
```

---

## ⚠️ Important: In-Memory Behavior

Phase-1 keeps all data **in memory**. Every **new Python process** starts empty.

Use **one** of the following so your data persists during a session:

### Option 1 — REPL (recommended for manual testing)

```bash
python repl.py
```

Then type one line at a time:

```
projects add --name "My Project" --description "Short description"
tasks add --project-id 1 --title "Write report" --status todo --deadline 2025-12-31
tasks status --project-id 1 --task-id 1 --status done
tasks list --project-id 1
projects delete --id 1
projects list
```

### Option 2 — One-shot (multiple commands in one process)

```bash
python -c 'from todolist.cli.app import main; \
main(["projects","add","--name","My Project","--description","Short description"]); \
main(["tasks","add","--project-id","1","--title","Write report","--status","todo","--deadline","2025-12-31"]); \
main(["tasks","status","--project-id","1","--task-id","1","--status","done"]); \
main(["tasks","list","--project-id","1"])'
```

### Option 3 — Standard CLI (each run is a fresh process)

Useful for quick, independent checks (remember: **no persistence** between calls):

```bash
python main.py --help
python main.py projects --help
python main.py tasks --help
```

---

## 🧭 CLI Reference

### Projects

```bash
python main.py projects add    --name "Alpha" --description "..."
python main.py projects edit   --id 1 --name "Alpha 2" --description "..."
python main.py projects delete --id 1
python main.py projects list
```

### Tasks (scoped to a project)

```bash
python main.py tasks add       --project-id 1 --title "Write report" --status todo --deadline 2025-12-31
python main.py tasks edit      --project-id 1 --task-id 1 --title "Revise" --status doing --deadline 2025-11-30
python main.py tasks status    --project-id 1 --task-id 1 --status done
python main.py tasks delete    --project-id 1 --task-id 1
python main.py tasks list      --project-id 1
```

---

## ✅ Rules & Validation

* **Statuses**: `todo` | `doing` | `done`
* **Title length**: ≤ 30 chars
* **Description length**: ≤ 150 chars
* **Deadline**: `YYYY-MM-DD` (e.g., `2025-12-31`)
* **Ceilings** (from `.env`)

  * `MAX_NUMBER_OF_PROJECT` → total projects
  * `MAX_NUMBER_OF_TASK` → per project
* **Cascade delete**: `projects delete` removes that project’s tasks.

---

## 🧪 Tests

Run the tiny smoke test:

```bash
pytest -q
```

---

## 🛠️ Troubleshooting

* **“ModuleNotFoundError: todolist”**
  Run commands **inside the project folder**, and (if using venv) **activate** it:

  ```bash
  cd ~/Downloads/todolist_phase1
  source .venv/bin/activate
  ```

* **Poetry not found**
  Use the venv+pip setup, or install Poetry (macOS: `brew install poetry`).

* **Data seems to disappear**
  You’re starting a **new process** for each command. Use the **REPL** or **one-shot** method so memory persists during your session.

* **zsh errors with `#` comments**
  Don’t paste lines with `#` into the REPL; they’re not treated as comments there (unless you modify `repl.py` to strip them).



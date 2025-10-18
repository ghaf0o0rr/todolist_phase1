import shlex
from todolist.cli.app import main

print("ToDoList REPL (Phase 1, in-memory). Type 'exit' to quit.")
while True:
    try:
        line = input("todolist> ").strip()
    except EOFError:
        break
    if not line or line.lower() in {"exit","quit"}:
        break
    if line.startswith("todolist> "):
        line = line[len("todolist> "):].strip()
    if "#" in line:
        line = line.split("#", 1)[0].strip()
    if not line:
        continue
    try:
        argv = shlex.split(line)
    except ValueError as e:
        print(f"[ERROR] {e}  (Tip: close your quotes or remove trailing comments)")
        continue
    try:
        main(argv)
    except SystemExit:
        pass

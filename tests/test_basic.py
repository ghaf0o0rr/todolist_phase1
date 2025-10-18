from todolist.core.services import ToDoService

def test_happy_flow():
    s = ToDoService()
    p = s.create_project("X", "desc")
    assert p.id == 1

    t = s.create_task(project_id=p.id, title="Do A", description="d", status="todo")
    assert t.id == 1

    s.change_task_status(project_id=p.id, task_id=t.id, status="done")
    assert s.list_tasks(p.id)[0].status.value == "done"

    s.delete_project(p.id)
    assert len(s.list_projects()) == 0

import logging
from orchestra.models import TodoListTemplate
from orchestra.models import Todo
from orchestra.models import Task

logger = logging.getLogger(__name__)


def add_todolist_template(todolist_template_id, task_id):
    todolist_template = TodoListTemplate.objects.get(id=todolist_template_id)
    task = Task.objects.get(id=task_id)
    template_todos = todolist_template.todos['items']
    parent_todo = Todo(
        task=task,
        description=todolist_template.name,
        template=todolist_template
    )
    parent_todo.save()
    for template_todo in template_todos:
        _add_template_todo(template_todo, todolist_template, parent_todo, task)


def _add_template_todo(template_todo, todolist_template, parent_todo, task):
    todo = Todo(
        task=task,
        description=template_todo['description'],
        template=todolist_template,
        parent_todo=parent_todo
    )
    todo.save()
    for template_todo_item in template_todo['items']:
        _add_template_todo(template_todo_item, todolist_template, todo, task)

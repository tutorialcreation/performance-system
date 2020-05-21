from taskmanager.views.auth import login, signup, logout
from taskmanager.views.teams import (
    team_create, team_detail, team_add_member, team_remove_member, team_delete
)
from taskmanager.views.index import index
from taskmanager.views.tasks import (
    task_create, tasks, completed_tasks, task_detail, task_edit,
    task_accept, task_mark_completed, task_comment, task_delete,send_push,view_push
)
from taskmanager.views.search import task_search

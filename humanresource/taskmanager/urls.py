"""Task Manager URL Configuration

"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from taskmanager import views

# from . import views

app_name = 'taskmanager'

urlpatterns = [
    path('', views.index, name='index'),
    path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
    path('teams/create/', views.team_create, name='team_create'),
    path('teams/<int:team_id>/remove-member/', views.team_remove_member, name='team_remove_member'),
    path('teams/<int:team_id>/add-member/', views.team_add_member, name='team_add_member'),
    path('teams/<int:team_id>/delete/', views.team_delete, name='team_delete'),
    path('my-tasks/', views.tasks, name='task_my_tasks'),
    path('my-completed-tasks/', views.completed_tasks, name='task_completed_tasks'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:task_id>/comment/', views.task_comment, name='task_comment'),
    path('tasks/<int:task_id>/accept/', views.task_accept, name='task_accept'),
    path('tasks/<int:task_id>/mark-completed/', views.task_mark_completed, name='task_mark_completed'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/search/', views.task_search, name='task_search'),
    # path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    # path('logout/', views.logout, name='logout'),
]

# urlpatterns += [
# ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from taskmanager.models import Team

UserModel = get_user_model()

@login_required
@require_http_methods(["GET", "POST"])
def team_create(request):
    """
    Any authenticated user can create team
    creator is leader of the team.
    """
    if request.method == 'POST':
        if request.POST.get('team_name'):
            team_name = request.POST['team_name']
            team = Team(name=team_name, leader_id=request.user.id)
            if request.POST.get('team_desc'):
                team.desc = request.POST['team_desc']
            team.save()
            team.members.add(request.user)
            messages.success(request, "New team `{0}` has created successfully!".format(team))
            # After creating team, redirect user to task_manager index page with success message
            return redirect('taskmanager:index')
        else:
            messages.error(request, "Missing required fields!")
            return redirect(request.path)
    else:
        return render(request, 'taskmanager/team_create.html', {'user' : request.user})

@login_required
@require_http_methods(["GET"])
def team_detail(request, team_id):
    """
    Any member of team is able to see team details
    Only team leader is able to add or remove members.
    """
    team = get_object_or_404(Team, id=team_id)
    tasks = team.task_set.exclude(status='COMP')
    if request.user in team.members.all():
        return render(
            request,
            'taskmanager/team_detail.html',
            {'user' : request.user, 'team' : team, 'tasks' : tasks}
        )
    else:
        raise PermissionDenied

@login_required
@require_http_methods(["GET"])
def team_add_member(request, team_id):
    """
    Only leader of team is allowed to add members to team using username.
    """
    team = get_object_or_404(Team, id=team_id)
    if request.user == team.leader:
        try:
            user = UserModel.objects.get(username=request.GET['username'])
            if user not in team.members.all():
                team.members.add(user)
                messages.success(request, "The user `{0}` has added to your team successfully!".format(user))
            else:
                messages.error(request, "The user `{0}` is already in team".format(user))
        except:
            messages.error(request, "User with username `{0}` is not found".format(request.GET['username']))
        return redirect(team)
    else:
        raise PermissionDenied

@login_required
@require_http_methods(["GET"])
def team_remove_member(request, team_id):
    """
    Only leader of team is allowed to remove members of team using username.
    """
    team = get_object_or_404(Team, id=team_id)
    if request.user == team.leader:
        try:
            user = team.members.get(username=request.GET.get('username'))
            if request.user == team.leader:
                if user != team.leader:
                    team.members.remove(user)
                    messages.success(request, "The user `{0}` has been removed from team".format(user))
                elif user == team.leader:
                    messages.error(request, "Leader can not be removed from team!")
        except:
            messages.error(request, "User with username `{0}` is not found in your team!".format(request.GET.get('username')))
        return redirect(team)
    else:
        raise PermissionDenied

@login_required
@require_http_methods(["GET"])
def team_delete(request, team_id):
    """
    Only team leader is allowed to the delete team.
    Team can only be deleted if it's members does not contain any other user except leader.
    """
    team = get_object_or_404(Team, id=team_id)
    if request.user == team.leader and team.members.count() == 1:
        team.delete()
        messages.success(request, "The team is deleted successfully!")
        # Team is deleted, redirect user to index page
        return redirect('taskmanager:index')
    else:
        raise PermissionDenied

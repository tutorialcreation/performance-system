from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from taskmanager.models import Task

@login_required
@require_http_methods(["GET"])
def task_search(request):
    """
    Search for tasks user has permission to see.
    """
    query_string = ""
    found_tasks = None
    if ("q" in request.GET) and request.GET["q"].strip():
        query_string = request.GET["q"]

        found_tasks = Task.objects.filter(
            (Q(title__icontains=query_string) | Q(desc__icontains=query_string)) &
            (Q(creator=request.user) | Q(assigned_to=request.user))
        ).distinct()
    else:
        messages.error(request, "Missing search parameter!")

    context = {"query_string": query_string, "found_tasks": found_tasks}
    return render(request, "taskmanager/task_search_results.html", context)

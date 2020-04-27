from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    logout as _logout,login as _login, authenticate, REDIRECT_FIELD_NAME, get_user_model,
)
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from taskmanager.forms.taskforms import SignUpForm

# Get User model defined in settings.AUTH_USER_MODEL
UserModel = get_user_model()

@require_http_methods(["GET", "POST"])
def login(request):
    """
    This view allows any unauthenticated user
    to login using username and password of any active User.
    Redirects to index page or REDIRECT_FIELD_NAME.
    """
    if request.user.is_authenticated:
        return redirect('taskmanager:index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            next = request.POST.get('next')
            if username and password:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if user.is_active:
                        _login(request, user)
                        if next:
                            return redirect(next)
                        else:
                            return redirect('taskmanager:index')
                    else:
                        messages.error(request, "This account is not active!")
                else:
                    messages.error(request, "Your username and password does not match!")
                    return redirect('taskmanager:login')
            else:
                messages.error(request, "Missing required fields!")
                return redirect('taskmanager:login')
        else:
            if request.GET.get(REDIRECT_FIELD_NAME):
                return render(
                    request,
                    'taskmanager/login.html',
                    {'user' : request.user, 'next' : request.GET[REDIRECT_FIELD_NAME]}
                )
            else:
                return render(request, 'taskmanager/login.html', {'user' : request.user})

@require_http_methods(["GET", "POST"])
def signup(request):
    """
    This view lets any unauthenticated user to
    create a User account.
    """
    if request.user.is_authenticated:
        return redirect('taskmanager:index')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                # If form is valid, save and login the user and redirect to index page
                user = form.save()
                _login(request, user)
                return redirect('taskmanager:index')
            else:
                # Form is not valid, send back to signup page with error messages
                return render(
                    request,
                    'taskmanager/signup.html',
                    {'user' : request.user, 'form' : form}
                )
        else:
            form = SignUpForm()
            return render(request, 'taskmanager/signup.html', {'user' : request.user, 'form' : form})

@login_required
@require_http_methods(["GET"])
def logout(request):
    """
    This view logs the user out and redirects to index page.
    """
    _logout(request)
    messages.success(request, "You have logged out succesfully!")
    return redirect('taskmanager:index')

import datetime

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

# Get user model defined in settings.AUTH_USER_MODEL
# Better to call get_user_model in pluggable app instead of imporing User from django.contrib.auth.models
UserModel = get_user_model()


class Team(models.Model):
    """
    Not using Django's built-in Group model because we want
    to save the creater of team.
    """
    name = models.CharField(max_length=50)
    desc = models.TextField(default='', max_length=1024, blank=True)
    leader = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='leading_teams')
    members = models.ManyToManyField(UserModel)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("taskmanager:team_detail", kwargs={"team_id": self.id})

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Teams"


class Task(models.Model):
    title = models.CharField(max_length=50)
    desc = models.TextField(default="", max_length=1024, blank=True)
    client_code = models.TextField(default="", max_length=1024, blank=True)
    client_name = models.TextField(default="", max_length=1024, blank=True)
    STATUS_CHOICES = (
        ('PLAN', 'Planned'),
        ('PROG', 'In Progress'),
        ('COMP', 'Completed')
    )
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='PLAN')

    creator = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='created_tasks')

    # A task can be assigned to one or many users
    assigned_to = models.ManyToManyField(UserModel, help_text="Press ctrl to select multiple")

    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    planned_date = models.DateField(auto_now_add=True)
    accepted_date = models.DateField(null=True, blank=True)
    accepted_by = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='accepted_tasks',
                                    blank=True)
    due_date = models.DateField()
    revised_due_date = models.DateField(null=True, blank=True)
    date_accepted = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("taskmanager:task_detail", kwargs={"task_id": self.id})

    # Has due date for an instance of this object passed?
    def is_overdated(self):
        """Returns whether the Tasks's due date has passed or not."""
        if self.due_date and datetime.date.today() > self.due_date:
            return True
        else:
            return False

    class Meta:
        ordering = ["planned_date"]
        verbose_name_plural = "Tasks"


class Comment(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment_datetime = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def snippet(self):
        """
        Returns a short version of comment body with auther's username as prefix
        """
        return "{author} - {snippet}...".format(author=self.author, snippet=self.body[:36])

    def __str__(self):
        return self.snippet()

    class Meta:
        ordering = ["-comment_datetime"]

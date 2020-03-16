import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taskmanager.models.tasks import Team, Task

UserModel = get_user_model()

class TaskModelTests(TestCase):

    def test_is_overdated_with_due_date_passed(self):
        """
        is_overdated() returns True for task whose due_date
        is passe
        """
        date = datetime.date.today()
        overdated_task = Task(title='Task1', due_date=date-datetime.timedelta(days=1))
        self.assertIs(overdated_task.is_overdated(), True)

    def test_is_overdated_with_date_not_passed(self):
        """
        is_overdated() returns Flse for task whose
        due_date is not passed
        """
        date = datetime.date.today()
        due_task = Task(title='Task2', due_date=date+datetime.timedelta(days=1))
        self.assertIs(due_task.is_overdated(), False)

class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.u1 = UserModel.objects.create(username='foo')
        cls.u2 = UserModel.objects.create(username='bar')
        cls.u3 = UserModel.objects.create(username='spam')
        cls.team1 = Team.objects.create(name='team1', leader=cls.u1)
        cls.team1.members.add(cls.u1)
        cls.team2 = Team.objects.create(name='team2', leader=cls.u2)
        cls.team2.members.add(cls.u2)
        cls.task1 = Task.objects.create(title='task1', creator=cls.u1, due_date=datetime.date.today())
        cls.task1.assigned_to.add(cls.u1)
        cls.task2 = Task.objects.create(title='task2', creator=cls.u2, due_date=datetime.date.today())
        cls.task2.assigned_to.add(cls.u2)

    def test_view_index(self):
        response = self.client.get(reverse('taskmanager:index'))
        self.assertEqual(response.status_code, 200)

    def test_view_login(self):
        response = self.client.get(reverse('taskmanager:login'))
        self.assertEqual(response.status_code, 200)

    def test_view_login_with_loggedin_user(self):
        self.client.force_login(self.u1)
        response = self.client.get(reverse('taskmanager:login'))
        self.assertEqual(response.status_code, 302)

    def test_view_signup(self):
        response = self.client.get(reverse('taskmanager:signup'))
        self.assertEqual(response.status_code, 200)

    def test_view_signup_with_loggedin_user(self):
        self.client.force_login(self.u1)
        response = self.client.get(reverse('taskmanager:signup'))
        self.assertEqual(response.status_code, 302)

    def test_view_team_create(self):
        """
        team_create view should redirect to index page after
        successfully creating team.
        """
        self.client.force_login(self.u1)
        url = reverse('taskmanager:team_create')
        response = self.client.post(url, {'team_name': 'team'})
        redirect_url = reverse('taskmanager:index')
        self.assertRedirects(response, redirect_url)

    def test_view_team_detail_with_no_permission(self):
        """
        team_detail should return 403 if user
        is not allowed to see that team.
        """
        self.client.force_login(self.u3)
        url = reverse('taskmanager:team_detail', kwargs={'team_id': self.team1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_view_team_detail_with_permission(self):
        """
        team_detail should return 200 if user
        is allowed to see that team.
        """
        self.client.force_login(self.u1)
        url = reverse('taskmanager:team_detail', kwargs={'team_id': self.team1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_team_add_member_without_permission(self):
        """
        team_add_member should return 403 if user is
        not leader of that team.
        """
        self.client.force_login(self.u3)
        url = reverse('taskmanager:team_add_member', kwargs={'team_id': self.team2.id})
        response = self.client.get(url, {'username': 'foo'})
        self.assertEqual(response.status_code, 403)

    def test_view_team_remove_member_with_permission(self):
        """
        team_remove_member should return 302
        after successfully removing member.
        """
        self.client.force_login(self.u2)
        team = Team.objects.create(name='team', leader=self.u2)
        team.members.add(self.u3)
        url = reverse('taskmanager:team_remove_member', kwargs={'team_id': team.id})
        response = self.client.get(url, {'username': 'spam'})
        self.assertEqual(response.status_code, 302)

    def test_view_delete_team(self):
        """
        Team can be deleted by team leader only if team has no members except leader.
        Redirects to index page after deletion.
        """
        self.client.force_login(self.u3)
        team = Team.objects.create(name='team', leader=self.u3)
        team.members.add(self.u3)
        url = reverse('taskmanager:team_delete', kwargs={'team_id': team.id})
        response = self.client.get(url)
        redirect_url = reverse('taskmanager:index')
        self.assertRedirects(response, redirect_url)

    def test_view_task_create(self):
        """
        task_create should redirect to task detail page after successfully creating task.
        """
        self.client.force_login(self.u1)
        url = reverse('taskmanager:task_create')
        response = self.client.post(url, {'title': 'task', 'due_date': datetime.date.today()})
        task = Task.objects.get(title='task')
        redirect_url = reverse('taskmanager:task_detail', kwargs={'task_id': task.id})
        self.assertRedirects(response, redirect_url)

    def test_view_task_edit_without_permission(self):
        """
        task_edit should return 403 if user is not creator of that task.
        """
        self.client.force_login(self.u1)
        url = reverse('taskmanager:task_edit', kwargs={'task_id': self.task2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_view_task_delete_without_permission(self):
        """
        task_delete should return 403 if user is not creator of that task.
        """
        self.client.force_login(self.u1)
        url = reverse('taskmanager:task_delete', kwargs={'task_id': self.task2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_view_task_delete_with_permission(self):
        """
        task_delete should redirect to index page after deleting task.
        """
        self.client.force_login(self.u1)
        task = Task.objects.create(title='task', creator=self.u1, due_date=datetime.date.today())
        url = reverse('taskmanager:task_delete', kwargs={'task_id': task.id})
        response = self.client.get(url)
        redirect_url = reverse('taskmanager:index')
        self.assertRedirects(response, redirect_url)

    def test_view_task_detail_without_permission(self):
        """
        task_detail should return 403 if user do not have permission to see that task.
        """
        self.client.force_login(self.u3)
        url = reverse('taskmanager:task_detail', kwargs={'task_id': self.task2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_view_task_comment_without_permission(self):
        """
        task_comment should return 403 if user do not have permission to see that task.
        """
        self.client.force_login(self.u3)
        url = reverse('taskmanager:task_comment', kwargs={'task_id': self.task2.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_view_task_comment_with_get(self):
        """
        task_comment should return 405 if user sends GET request.
        """
        self.client.force_login(self.u3)
        url = reverse('taskmanager:task_comment', kwargs={'task_id': self.task2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

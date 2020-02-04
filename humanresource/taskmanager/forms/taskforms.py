from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth import authenticate

from taskmanager.models import *

# Get the user model defined in setting.AUTH_USER_MODEL
UserModel = get_user_model()

class TaskCreationForm(ModelForm):

    due_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "w3-input"})
    )

    revised_due_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "w3-input"})
    )

    date_accepted = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "w3-input"})
    )

    desc = forms.CharField(
        label="Description",
        widget=forms.Textarea(
            attrs={"class": "w3-input", "placeholder": "Describe about task", "rows": 5}
        ),
        required=False
    )
    client_code = forms.CharField(
        label="Client Code",
        widget=forms.TextInput(
            attrs={"class": "w3-input", "placeholder": "Client code", "rows": 5}
        ),
        required=False
    )
    client_name = forms.CharField(
        label="Client Name",
        widget=forms.TextInput(
            attrs={"class": "w3-input", "placeholder": "Client name", "rows": 5}
        ),
        required=False
    )

    class Meta:
        model = Task
        fields = ('title','date_accepted','due_date','revised_due_date','team')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {"class": "w3-input", "placeholder": "Enter title for task"}
        )
        self.fields["team"].widget.attrs.update({"class": "w3-input"})
        self.fields["team"].queryset = kwargs.get('initial').get('teams')


class TaskEditForm(ModelForm):

    due_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "w3-input"})
    )

    desc = forms.CharField(
        label="Description",
        widget=forms.Textarea(
            attrs={"class": "w3-input", "placeholder": "Describe about task", "rows": 5}
        ),
        required=False
    )

    class Meta:
        model = Task
        fields = ('title', 'desc', 'due_date', 'team', 'assigned_to')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {"class": "w3-input", "placeholder": "Enter title for task"}
        )
        self.fields["assigned_to"].widget.attrs.update({"class": "w3-select"})
        self.fields["team"].widget.attrs.update({"class": "w3-select"})
        if kwargs.get('initial').get('has_team'):
            # We don't want user to edit assigned team, if it is already assigned to one team
            del self.fields["team"]
            self.fields["assigned_to"].queryset = kwargs.get('initial').get('members')
        else:
            # If task is still not assigned to any team, there us no need of assigned_to field
            del self.fields["assigned_to"]
            self.fields["team"].queryset = kwargs.get('initial').get('teams')


class SignUpForm(forms.ModelForm):
    """
    A form that creates a user, from the given username, email and
    password.
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "w3-input", "placeholder": "Make this a good one!"}
        ),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(
            attrs={"class": "w3-input", "placeholder": "Enter same Password, for verification"}
        ),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = UserModel
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"autofocus": True, "class": "w3-input", "placeholder": "Create a unique username for you!"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "w3-input", "required": True, "placeholder": "Enter your email address"}
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


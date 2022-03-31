from django.contrib.auth import forms, models


class UserForm(forms.UserCreationForm):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'username', 'password1')

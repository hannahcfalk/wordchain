from django.contrib.auth import forms, models


class SignUpForm(forms.UserCreationForm):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'username', 'password1')

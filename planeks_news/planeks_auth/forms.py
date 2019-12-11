from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'birth_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget = DateInput()
        self.fields['birth_date'].label = 'Дата рождения'


class UserLoginForm(AuthenticationForm):
    model = User

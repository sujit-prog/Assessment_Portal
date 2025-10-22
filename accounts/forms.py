from django import forms
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    """
    A custom form for user registration that extends Django's built-in UserCreationForm.
    """
    class Meta(UserCreationForm.Meta):
        # We can add extra fields here if needed.
        # By default, it includes username, password, and password confirmation.
        fields = UserCreationForm.Meta.fields
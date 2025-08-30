from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    """
    Extended user creation form that includes email field.
    """
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.'
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional.'
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional.'
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes for styling
        for fieldname in ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']:
            self.fields[fieldname].widget.attrs['class'] = 'form-control'


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes for styling
        for fieldname in ['username', 'first_name', 'last_name', 'email']:
            self.fields[fieldname].widget.attrs['class'] = 'form-control'

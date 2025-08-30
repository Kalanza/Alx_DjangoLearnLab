from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post

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


class PostForm(forms.ModelForm):
    """
    Form for creating and updating blog posts.
    """
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title...',
                'maxlength': '200'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 10,
                'style': 'resize: vertical;'
            })
        }
        help_texts = {
            'title': 'Maximum 200 characters',
            'content': 'Write your blog post content. You can use plain text or HTML.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom validation and styling
        self.fields['title'].required = True
        self.fields['content'].required = True

    def clean_title(self):
        """Custom validation for title field."""
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 5:
                raise forms.ValidationError('Title must be at least 5 characters long.')
        return title

    def clean_content(self):
        """Custom validation for content field."""
        content = self.cleaned_data.get('content')
        if content:
            content = content.strip()
            if len(content) < 20:
                raise forms.ValidationError('Content must be at least 20 characters long.')
        return content

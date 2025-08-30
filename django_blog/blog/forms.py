from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag

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
    Form for creating and updating blog posts with tags.
    """
    tags_input = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (e.g., python, django, web)',
            'data-toggle': 'tooltip',
            'title': 'Add tags to categorize your post'
        }),
        help_text='Enter tags separated by commas. New tags will be created automatically.'
    )

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
        
        # Pre-populate tags if editing existing post
        if self.instance and self.instance.pk:
            existing_tags = [tag.name for tag in self.instance.tags.all()]
            self.fields['tags_input'].initial = ', '.join(existing_tags)

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

    def clean_tags_input(self):
        """Clean and validate tags input."""
        tags_input = self.cleaned_data.get('tags_input', '')
        if tags_input:
            # Split by comma and clean each tag
            tags = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]
            # Remove duplicates while preserving order
            unique_tags = []
            for tag in tags:
                if tag not in unique_tags and len(tag) <= 50:  # Max length validation
                    unique_tags.append(tag)
            return unique_tags
        return []

    def save(self, commit=True):
        """Save post and handle tags."""
        post = super().save(commit=commit)
        
        if commit:
            # Clear existing tags
            post.tags.clear()
            
            # Process tags
            tags_list = self.cleaned_data.get('tags_input', [])
            for tag_name in tags_list:
                if tag_name:  # Only process non-empty tags
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)
        
        return post


class SearchForm(forms.Form):
    """
    Form for searching posts by title, content, or tags.
    """
    query = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search posts by title, content, or tags...',
            'autocomplete': 'off'
        }),
        help_text='Enter keywords to search for posts'
    )
    
    search_in = forms.MultipleChoiceField(
        choices=[
            ('title', 'Title'),
            ('content', 'Content'),
            ('tags', 'Tags'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        initial=['title', 'content', 'tags'],
        required=False,
        help_text='Select where to search (default: all)'
    )

    def clean_query(self):
        """Clean and validate search query."""
        query = self.cleaned_data.get('query', '')
        if query:
            query = query.strip()
            if len(query) < 2:
                raise forms.ValidationError('Search query must be at least 2 characters long.')
        return query


class CommentForm(forms.ModelForm):
    """
    Form for creating and updating comments.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4,
                'style': 'resize: vertical;'
            })
        }
        help_texts = {
            'content': 'Share your thoughts about this post.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = True
        self.fields['content'].label = 'Comment'

    def clean_content(self):
        """Custom validation for content field."""
        content = self.cleaned_data.get('content')
        if content:
            content = content.strip()
            if len(content) < 5:
                raise forms.ValidationError('Comment must be at least 5 characters long.')
            if len(content) > 1000:
                raise forms.ValidationError('Comment must be less than 1000 characters long.')
        return content

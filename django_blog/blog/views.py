from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Post
from .forms import CustomUserCreationForm, UserUpdateForm

# Create your views here.

def home(request):
    """
    Home page view displaying recent blog posts.
    """
    posts = Post.objects.all()[:5]  # Get the 5 most recent posts
    return render(request, 'blog/home.html', {'posts': posts})

def posts_list(request):
    """
    View to display all blog posts.
    """
    posts = Post.objects.all()
    return render(request, 'blog/posts_list.html', {'posts': posts})

def register_view(request):
    """
    User registration view using custom registration form.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            login(request, user)  # Automatically log in the user after registration
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile_view(request):
    """
    User profile view that allows viewing and editing profile information.
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'blog/profile.html', context)

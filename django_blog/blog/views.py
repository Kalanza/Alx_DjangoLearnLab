from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.urls import reverse_lazy
from .models import Post
from .forms import CustomUserCreationForm, UserUpdateForm

# Create your views here.

def home(request):
    """
    Home page view displaying recent blog posts.
    """
    posts = Post.objects.all()[:5]  # Get the 5 most recent posts
    return render(request, 'blog/home.html', {'posts': posts})

# Authentication Views
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

# Blog Post CRUD Views
class PostListView(ListView):
    """
    Display all blog posts with pagination.
    """
    model = Post
    template_name = 'blog/post_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-published_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Blog Posts'
        return context

class PostDetailView(DetailView):
    """
    Display individual blog post details.
    """
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to create new blog posts.
    """
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        """Set the author to the current user before saving."""
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Post'
        context['button_text'] = 'Create Post'
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow post authors to edit their posts.
    """
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        """Set the author to the current user before saving."""
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        """Check if the current user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Post'
        context['button_text'] = 'Update Post'
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allow post authors to delete their posts.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        """Check if the current user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        """Add success message when post is deleted."""
        messages.success(self.request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Post'
        return context

# User's posts view
class UserPostListView(ListView):
    """
    Display all posts by a specific user.
    """
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        from django.contrib.auth.models import User
        user = User.objects.get(username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.contrib.auth.models import User
        user = User.objects.get(username=self.kwargs.get('username'))
        context['title'] = f"Posts by {user.username}"
        context['post_author'] = user
        return context

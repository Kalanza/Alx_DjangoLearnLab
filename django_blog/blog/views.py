from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Count
from .models import Post, Comment, Tag
from .forms import CustomUserCreationForm, UserUpdateForm, CommentForm, PostForm, SearchForm

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
    Display individual blog post details with comments.
    """
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        # Add comments to context
        context['comments'] = self.object.comments.all().order_by('created_at')
        # Add comment form for authenticated users
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to create new blog posts with tags.
    """
    model = Post
    form_class = PostForm
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
    Allow post authors to edit their posts and tags.
    """
    model = Post
    form_class = PostForm
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


# Comment Views
class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to create comments on blog posts.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        """Set the author and post before saving."""
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        messages.success(self.request, 'Your comment has been added successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the post detail page after creating comment."""
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        context['title'] = 'Add Comment'
        return context


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow comment authors to edit their comments.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        """Check if the current user is the author of the comment."""
        comment = self.get_object()
        return self.request.user == comment.author

    def form_valid(self, form):
        """Add success message when comment is updated."""
        messages.success(self.request, 'Your comment has been updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the post detail page after updating comment."""
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object.post
        context['title'] = 'Edit Comment'
        return context


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allow comment authors to delete their comments.
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        """Check if the current user is the author of the comment."""
        comment = self.get_object()
        return self.request.user == comment.author

    def delete(self, request, *args, **kwargs):
        """Add success message when comment is deleted."""
        messages.success(self.request, 'Your comment has been deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        """Redirect to the post detail page after deleting comment."""
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Comment'
        return context


@login_required
def add_comment(request, post_id):
    """
    Function-based view to handle comment creation via AJAX or regular form submission.
    """
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment has been added successfully!')
            return redirect('post-detail', pk=post_id)
    else:
        form = CommentForm()
    
    return render(request, 'blog/add_comment.html', {
        'form': form,
        'post': post,
        'title': 'Add Comment'
    })


# Search and Tag Views
class SearchResultsView(ListView):
    """
    Display search results based on user query.
    """
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        """Filter posts based on search query."""
        form = SearchForm(self.request.GET)
        queryset = Post.objects.none()

        if form.is_valid():
            query = form.cleaned_data['query']
            search_in = form.cleaned_data.get('search_in', ['title', 'content', 'tags'])

            if query:
                # Build Q objects for different search criteria
                q_objects = Q()

                if 'title' in search_in:
                    q_objects |= Q(title__icontains=query)
                
                if 'content' in search_in:
                    q_objects |= Q(content__icontains=query)
                
                if 'tags' in search_in:
                    q_objects |= Q(tags__name__icontains=query)

                queryset = Post.objects.filter(q_objects).distinct().order_by('-published_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SearchForm(self.request.GET)
        context['form'] = form
        context['query'] = self.request.GET.get('query', '')
        context['title'] = f'Search Results for "{context["query"]}"' if context['query'] else 'Search Results'
        return context


class PostsByTagView(ListView):
    """
    Display all posts filtered by a specific tag.
    """
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        """Filter posts by tag name."""
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tags__name__iexact=tag_name).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_name = self.kwargs.get('tag_name')
        context['tag'] = get_object_or_404(Tag, name__iexact=tag_name)
        context['title'] = f'Posts tagged with "{tag_name}"'
        return context


def search_posts(request):
    """
    Function-based search view that handles both GET and POST requests.
    """
    form = SearchForm(request.GET or None)
    posts = []
    query = ''

    if request.method == 'GET' and form.is_valid():
        query = form.cleaned_data['query']
        search_in = form.cleaned_data.get('search_in', ['title', 'content', 'tags'])

        if query:
            # Build Q objects for complex queries
            q_objects = Q()

            if 'title' in search_in:
                q_objects |= Q(title__icontains=query)
            
            if 'content' in search_in:
                q_objects |= Q(content__icontains=query)
            
            if 'tags' in search_in:
                q_objects |= Q(tags__name__icontains=query)

            posts = Post.objects.filter(q_objects).distinct().order_by('-published_date')

    context = {
        'form': form,
        'posts': posts,
        'query': query,
        'title': f'Search Results for "{query}"' if query else 'Search Posts'
    }

    return render(request, 'blog/search.html', context)


class TagListView(ListView):
    """
    Display all available tags with post counts.
    """
    model = Tag
    template_name = 'blog/tag_list.html'
    context_object_name = 'tags'
    paginate_by = 20

    def get_queryset(self):
        return Tag.objects.annotate(
            post_count=Count('posts')
        ).filter(post_count__gt=0).order_by('-post_count', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Tags'
        
        # Get tags with post counts and recent posts
        tags_with_data = []
        max_count = 0
        min_count = float('inf')
        total_posts = 0
        
        for tag in self.get_queryset():
            post_count = tag.post_count
            max_count = max(max_count, post_count)
            min_count = min(min_count, post_count)
            total_posts += post_count
            
            # Get recent posts for this tag
            recent_posts = tag.posts.order_by('-published_date')[:3]
            
            tags_with_data.append({
                'tag': tag,
                'count': post_count,
                'recent_posts': recent_posts,
            })
        
        # Calculate font sizes for tag cloud (between 0.8 and 2.5 rem)
        if max_count > min_count:
            for tag_data in tags_with_data:
                count = tag_data['count']
                # Scale font size based on post count
                font_size = 0.8 + (count - min_count) / (max_count - min_count) * 1.7
                tag_data['font_size'] = round(font_size, 1)
        else:
            for tag_data in tags_with_data:
                tag_data['font_size'] = 1.5
        
        # Find most used tag
        most_used_tag = None
        if tags_with_data:
            most_used_tag = max(tags_with_data, key=lambda x: x['count'])
        
        context['tags'] = tags_with_data
        context['total_posts'] = total_posts
        context['most_used_tag'] = most_used_tag
        
        return context

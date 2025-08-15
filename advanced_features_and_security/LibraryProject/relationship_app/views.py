# ============================================================================
# RELATIONSHIP APP VIEWS
# ============================================================================
# This module contains all views for the relationship_app Django application
# including library management views and user authentication views
# ============================================================================

# ============================================================================
# IMPORTS
# ============================================================================

# Django Core Imports
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy

# Django Class-Based Views
from django.views.generic.detail import DetailView
from django.views.generic import CreateView

# Django Authentication Imports
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404

# Local Model Imports
from .models import Library, Book, Author

# ============================================================================
# LIBRARY MANAGEMENT VIEWS
# ============================================================================

def home(request):
    """
    Home page view with navigation to different sections.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered home page template
    """
    return render(request, 'relationship_app/home.html')


def list_books(request):
    """
    Function-based view that lists all books using a template.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered template with all books from the database
    """
    books = Book.objects.all()  # Fetch all book instances from the database
    
    # Pass the books to the template
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)


class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library,
    listing all books in that library.
    
    Attributes:
        model: Library model to display
        template_name: Template used for rendering
        context_object_name: Name of the object in template context
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        """
        Add books in the library to the context.
        
        Args:
            **kwargs: Additional keyword arguments
            
        Returns:
            Updated context dictionary with library books
        """
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        context['books'] = library.books.all()
        return context


# ============================================================================
# USER AUTHENTICATION VIEWS
# ============================================================================
# These views handle user registration, login, and logout functionality
# using Django's built-in authentication system
# ============================================================================

class SignUpView(CreateView):
    """
    User registration view using Django's built-in UserCreationForm.
    
    This view handles new user registration and redirects to login page
    upon successful account creation.
    
    Attributes:
        form_class: Django's built-in UserCreationForm
        success_url: URL to redirect to after successful registration
        template_name: Template used for registration form
    """
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'relationship_app/register.html'


def register(request):
    """
    Function-based view for user registration using Django's built-in UserCreationForm.
    
    This view handles both GET and POST requests for user registration.
    On GET: displays the registration form
    On POST: processes the form and creates a new user
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered registration template or redirect to login page
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})


class CustomLoginView(LoginView):
    """
    Custom login view utilizing Django's built-in LoginView.
    
    This view handles user authentication and login functionality
    with custom template and redirect behavior.
    
    Attributes:
        template_name: Template used for login form
        redirect_authenticated_user: Whether to redirect already logged-in users
    """
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """
        Determine the URL to redirect to after successful login.
        
        Returns:
            URL to redirect to (home page)
        """
        return reverse_lazy('home')     


class CustomLogoutView(LogoutView):
    """
    Custom logout view utilizing Django's built-in LogoutView.
    
    This view handles user logout and redirects to home page
    after successful logout.
    
    Attributes:
        next_page: URL to redirect to after logout
    """
    next_page = reverse_lazy('home')

# ============================================================================
# CUSTOM PERMISSIONS VIEWS
# ============================================================================
# These views handle book creation, modification, and deletion with custom permissions
# ============================================================================

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """
    View to add a new book - requires 'can_add_book' permission.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered add book template or redirect after successful creation
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author_id')
        
        if title and author_id:
            try:
                author = Author.objects.get(id=author_id)
                book = Book.objects.create(title=title, author=author)
                return redirect('list_books')
            except Author.DoesNotExist:
                pass
    
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    """
    View to edit an existing book - requires 'can_change_book' permission.
    
    Args:
        request: HTTP request object
        book_id: ID of the book to edit
        
    Returns:
        Rendered edit book template or redirect after successful update
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author_id')
        
        if title and author_id:
            try:
                author = Author.objects.get(id=author_id)
                book.title = title
                book.author = author
                book.save()
                return redirect('list_books')
            except Author.DoesNotExist:
                pass
    
    authors = Author.objects.all()
    return render(request, 'relationship_app/edit_book.html', {
        'book': book,
        'authors': authors
    })


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    """
    View to delete a book - requires 'can_delete_book' permission.
    
    Args:
        request: HTTP request object
        book_id: ID of the book to delete
        
    Returns:
        Rendered delete confirmation template or redirect after deletion
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})


# ============================================================================
# ROLE-BASED ACCESS CONTROL VIEWS
# ============================================================================

from django.contrib.auth.decorators import user_passes_test
from bookshelf.models import UserProfile

def is_admin(user):
    """Check if user has Admin role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    """Check if user has Librarian role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    """Check if user has Member role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    """Admin view - only accessible by users with Admin role."""
    return render(request, 'admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    """Librarian view - only accessible by users with Librarian role."""
    return render(request, 'librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    """Member view - only accessible by users with Member role."""
    return render(request, 'member_view.html')

# ============================================================================
# END OF VIEWS
# ============================================================================
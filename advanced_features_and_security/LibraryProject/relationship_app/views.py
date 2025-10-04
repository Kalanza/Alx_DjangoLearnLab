from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.decorators import login_required
from .models import Book, Author

def register(request):
    """Function-based view for user registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Redirect based on user role
            try:
                role = user.userprofile.role
                if role == 'Admin':
                    return redirect('admin_view')
                elif role == 'Librarian':
                    return redirect('librarian_view')
                else:  # Member
                    return redirect('member_view')
            except:
                # Fallback if no profile exists yet
                return redirect('member_view')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# Role-checking functions
def is_admin(user):
    """Check if user has Admin role"""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    """Check if user has Librarian role"""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    """Check if user has Member role"""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Role-based views
@user_passes_test(is_admin)
def admin_view(request):
    """View for Admin users only"""
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    """View for Librarian users only"""
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    """View for Member users only"""
    return render(request, 'relationship_app/member_view.html')

# Book management views with permission decorators
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """View to add a new book - requires can_add_book permission"""
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        if title and author_id:
            author = get_object_or_404(Author, id=author_id)
            Book.objects.create(title=title, author=author)
            return redirect('book_list')  # Redirect to book list after adding
    
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    """View to edit an existing book - requires can_change_book permission"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        if title and author_id:
            author = get_object_or_404(Author, id=author_id)
            book.title = title
            book.author = author
            book.save()
            return redirect('book_list')  # Redirect to book list after editing
    
    authors = Author.objects.all()
    return render(request, 'relationship_app/edit_book.html', {
        'book': book,
        'authors': authors
    })

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    """View to delete a book - requires can_delete_book permission"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')  # Redirect to book list after deletion
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})

# Book listing view (no special permissions required for viewing)
def book_list(request):
    """View to list all books - no special permissions required"""
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})
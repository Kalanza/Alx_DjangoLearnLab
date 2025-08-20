"""
Secure views for the bookshelf application.
Implements security best practices including:
- CSRF protection through Django forms
- Input validation and sanitization
- SQL injection prevention through ORM usage
- Permission-based access control
- Secure handling of user data
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.html import escape
from .models import Book
from .forms import BookForm, BookSearchForm, ExampleForm
from django.urls import reverse

# Create your views here.

@permission_required('bookshelf.can_view', raise_exception=True)
@never_cache  # Prevent caching of sensitive data
def book_list(request):
    """
    Secure view to display all books with search functionality.
    Includes pagination and safe search handling to prevent SQL injection.
    Requires 'can_view' permission.
    """
    books = Book.objects.all()
    search_form = BookSearchForm(request.GET or None)
    
    # Handle secure search functionality
    if search_form.is_valid() and search_form.cleaned_data.get('search_query'):
        query = search_form.cleaned_data['search_query']
        search_type = search_form.cleaned_data.get('search_type', 'all')
        
        # Use Django ORM to prevent SQL injection
        if search_type == 'title':
            books = books.filter(title__icontains=query)
        elif search_type == 'author':
            books = books.filter(author__icontains=query)
        elif search_type == 'year':
            try:
                year = int(query)
                books = books.filter(publication_year=year)
            except ValueError:
                messages.warning(request, 'Invalid year format.')
        else:  # search_type == 'all'
            books = books.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query)
            )
    
    # Implement pagination for better performance
    paginator = Paginator(books, 10)  # Show 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_books': books.count()
    }
    return render(request, 'bookshelf/book_list.html', context)

@permission_required('bookshelf.can_view', raise_exception=True)
@never_cache
def book_detail(request, pk):
    """
    Secure view to display a single book.
    Uses get_object_or_404 to safely handle non-existent objects.
    Requires 'can_view' permission.
    """
    # Validate pk parameter to prevent injection
    try:
        pk = int(pk)
    except (ValueError, TypeError):
        messages.error(request, 'Invalid book ID.')
        return redirect('book_list')
    
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

@permission_required('bookshelf.can_create', raise_exception=True)
@csrf_protect  # Explicit CSRF protection
@require_http_methods(["GET", "POST"])  # Only allow GET and POST
def book_create(request):
    """
    Secure view to create a new book using Django forms.
    Implements CSRF protection and input validation.
    Requires 'can_create' permission.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # Use form.save() for secure data handling
            book = form.save()
            messages.success(request, f'Book "{escape(book.title)}" created successfully!')
            return redirect('book_detail', pk=book.pk)
        else:
            # Form validation failed - errors will be displayed in template
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'form_title': 'Create Book'
    })

@permission_required('bookshelf.can_edit', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def book_edit(request, pk):
    """
    Secure view to edit an existing book using Django forms.
    Implements CSRF protection and input validation.
    Requires 'can_edit' permission.
    """
    # Validate pk parameter
    try:
        pk = int(pk)
    except (ValueError, TypeError):
        messages.error(request, 'Invalid book ID.')
        return redirect('book_list')
    
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            updated_book = form.save()
            messages.success(request, f'Book "{escape(updated_book.title)}" updated successfully!')
            return redirect('book_detail', pk=updated_book.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'book': book,
        'form_title': 'Edit Book'
    })

@permission_required('bookshelf.can_delete', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def book_delete(request, pk):
    """
    Secure view to delete a book with confirmation.
    Implements CSRF protection and safe deletion.
    Requires 'can_delete' permission.
    """
    # Validate pk parameter
    try:
        pk = int(pk)
    except (ValueError, TypeError):
        messages.error(request, 'Invalid book ID.')
        return redirect('book_list')
    
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book_title = escape(book.title)  # Escape for safe display
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# Security utility view for CSP reporting (optional)
@csrf_protect
def csp_report(request):
    """
    Handle Content Security Policy violation reports.
    This helps monitor and improve security.
    """
    if request.method == 'POST':
        # Log CSP violations for security monitoring
        # In production, you might want to log this to a security monitoring system
        import logging
        logger = logging.getLogger('security.csp')
        logger.warning(f'CSP violation reported: {request.body}')
    
    return HttpResponse(status=204)  # No content response

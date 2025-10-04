"""
Example views demonstrating permission-based access control.
This shows how to use the custom permissions in Django views.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Book

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View to list all books - requires 'can_view' permission
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    View to create a new book - requires 'can_create' permission
    """
    if request.method == 'POST':
        # Handle book creation logic here
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        
        book = Book.objects.create(
            title=title,
            author=author,
            publication_year=int(publication_year) if publication_year else None
        )
        messages.success(request, f'Book "{book.title}" created successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_create.html')

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, book_id):
    """
    View to edit a book - requires 'can_edit' permission
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        # Handle book editing logic here
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        book.publication_year = request.POST.get('publication_year', book.publication_year)
        book.save()
        
        messages.success(request, f'Book "{book.title}" updated successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_edit.html', {'book': book})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, book_id):
    """
    View to delete a book - requires 'can_delete' permission
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_delete.html', {'book': book})

@login_required
def check_user_permissions(request):
    """
    Helper view to show what permissions the current user has
    """
    user = request.user
    permissions = {
        'can_view': user.has_perm('bookshelf.can_view'),
        'can_create': user.has_perm('bookshelf.can_create'),
        'can_edit': user.has_perm('bookshelf.can_edit'),
        'can_delete': user.has_perm('bookshelf.can_delete'),
    }
    
    user_groups = [group.name for group in user.groups.all()]
    
    context = {
        'permissions': permissions,
        'user_groups': user_groups,
        'user': user
    }
    
    return render(request, 'bookshelf/user_permissions.html', context)
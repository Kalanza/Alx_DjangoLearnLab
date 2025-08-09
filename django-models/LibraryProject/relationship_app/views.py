from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book

# Create your views here.

def home(request):
    """Home page view with navigation to different sections."""
    return render(request, 'relationship_app/home.html')

def list_books(request):
    """Function-based view that lists all books using a template."""
    books = Book.objects.all()  # Fetch all book instances from the database
    
    # Pass the books to the template
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    """Class-based view that displays details for a specific library, listing all books in that library."""
    model = Library
    template_name = 'relationship_app/library_detail.html'  # Updated template path
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        """Add books in the library to the context."""
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        context['books'] = library.books.all()
        return context 
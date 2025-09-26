from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def check_role(user, role):
    """Helper function to check if user has the required role"""
    return hasattr(user, 'userprofile') and user.userprofile.role == role

def is_librarian(user):
    """Check if user has Librarian role"""
    return check_role(user, 'Librarian')

@user_passes_test(is_librarian)
def librarian_view(request):
    """View accessible only to Librarian users"""
    return render(request, 'relationship_app/librarian_view.html', {
        'user': request.user,
        'role': request.user.userprofile.role
    })

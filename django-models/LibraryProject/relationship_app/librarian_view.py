# ============================================================================
# LIBRARIAN VIEW
# ============================================================================
# This module contains the librarian view for role-based access control
# Only users with 'Librarian' role can access this view
# ============================================================================

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile


def is_librarian(user):
    """
    Check if user has Librarian role.
    
    Args:
        user: Django User object
        
    Returns:
        bool: True if user is authenticated and has Librarian role, False otherwise
    """
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.LIBRARIAN


@user_passes_test(is_librarian)
def librarian_view(request):
    """
    Librarian dashboard view - only accessible by users with Librarian role.
    
    This view provides library management functionality and content
    that should only be available to users with librarian privileges.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered librarian dashboard template
    """
    return render(request, 'librarian_view.html')

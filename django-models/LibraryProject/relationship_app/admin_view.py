# ============================================================================
# ADMIN VIEW
# ============================================================================
# This module contains the admin view for role-based access control
# Only users with 'Admin' role can access this view
# ============================================================================

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile


def is_admin(user):
    """
    Check if user has Admin role.
    
    Args:
        user: Django User object
        
    Returns:
        bool: True if user is authenticated and has Admin role, False otherwise
    """
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.ADMIN


@user_passes_test(is_admin)
def admin_view(request):
    """
    Admin dashboard view - only accessible by users with Admin role.
    
    This view provides administrative functionality and content
    that should only be available to users with administrative privileges.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered admin dashboard template
    """
    return render(request, 'admin_view.html')

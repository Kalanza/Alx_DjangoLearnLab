# ============================================================================
# MEMBER VIEW
# ============================================================================
# This module contains the member view for role-based access control
# Only users with 'Member' role can access this view
# ============================================================================

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile


def is_member(user):
    """
    Check if user has Member role.
    
    Args:
        user: Django User object
        
    Returns:
        bool: True if user is authenticated and has Member role, False otherwise
    """
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.MEMBER


@user_passes_test(is_member)
def member_view(request):
    """
    Member dashboard view - only accessible by users with Member role.
    
    This view provides member-specific functionality and content
    that should only be available to users with member privileges.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered member dashboard template
    """
    return render(request, 'member_view.html')

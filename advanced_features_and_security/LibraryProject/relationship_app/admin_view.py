from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile

def is_admin(user):
    """Check if the user has the Admin role."""
    return (
        user.is_authenticated
        and hasattr(user, 'userprofile')
        and user.userprofile.role == 'Admin'
    )

@user_passes_test(is_admin)
def admin_view(request):
    """Admin dashboard - accessible only to Admin role."""
    return render(request, 'admin_view.html')

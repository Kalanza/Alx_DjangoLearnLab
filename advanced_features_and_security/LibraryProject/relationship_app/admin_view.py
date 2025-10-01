from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def check_role(user, role):
    """Helper function to check if user has the required role"""
    return hasattr(user, 'userprofile') and user.userprofile.role == role

def is_admin(user):
    """Check if user has Admin role"""
    return check_role(user, 'Admin')

@user_passes_test(is_admin)
def admin_view(request):
    """View accessible only to Admin users"""
    return render(request, 'relationship_app/admin_view.html', {
        'user': request.user,
        'role': request.user.userprofile.role
    })

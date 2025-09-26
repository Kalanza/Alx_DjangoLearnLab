from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def check_role(user, role):
    """Helper function to check if user has the required role"""
    return hasattr(user, 'userprofile') and user.userprofile.role == role

def is_member(user):
    """Check if user has Member role"""
    return check_role(user, 'Member')

@user_passes_test(is_member)
def member_view(request):
    """View accessible only to Member users"""
    return render(request, 'relationship_app/member_view.html', {
        'user': request.user,
        'role': request.user.userprofile.role
    })

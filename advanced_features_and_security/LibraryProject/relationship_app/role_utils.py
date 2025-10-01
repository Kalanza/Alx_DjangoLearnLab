from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile

@login_required
def role_redirect_view(request):
    """Redirect users to their appropriate dashboard based on role"""
    try:
        role = request.user.userprofile.role
        if role == 'Admin':
            return redirect('admin_view')
        elif role == 'Librarian':
            return redirect('librarian_view')
        else:  # Member
            return redirect('member_view')
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist (fallback)
        UserProfile.objects.create(user=request.user, role='Member')
        return redirect('member_view')

@login_required
def dashboard(request):
    """Main dashboard that redirects based on user role"""
    return role_redirect_view(request)
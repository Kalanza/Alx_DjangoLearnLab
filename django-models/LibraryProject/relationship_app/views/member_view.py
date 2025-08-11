from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile

def is_member(user):
    """Check if the user has the Member role."""
    return (
        user.is_authenticated
        and hasattr(user, 'userprofile')
        and user.userprofile.role == UserProfile.MEMBER
    )

@user_passes_test(is_member)
def member_view(request):
    """Member dashboard - accessible only to Member role."""
    return render(request, 'member_view.html')

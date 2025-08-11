from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile

def is_librarian(user):
    """Check if the user has the Librarian role."""
    return (
        user.is_authenticated
        and hasattr(user, 'userprofile')
        and user.userprofile.role == UserProfile.LIBRARIAN
    )

@user_passes_test(is_librarian)
def librarian_view(request):
    """Librarian dashboard - accessible only to Librarian role."""
    return render(request, 'librarian_view.html')

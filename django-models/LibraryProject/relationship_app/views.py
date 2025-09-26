from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, logout

def register(request):
    """Function-based view for user registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Redirect based on user role
            try:
                role = user.userprofile.role
                if role == 'Admin':
                    return redirect('admin_view')
                elif role == 'Librarian':
                    return redirect('librarian_view')
                else:  # Member
                    return redirect('member_view')
            except:
                # Fallback if no profile exists yet
                return redirect('member_view')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
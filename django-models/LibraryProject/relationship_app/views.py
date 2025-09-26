from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login ,logout

class SignUpView(CreateView):
    form = UserCreationForm
    success_urk= reverse_lazy('login')
    template_name = ('signup/registration.html')
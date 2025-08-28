from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'blog/base.html')

def posts(request):
    return HttpResponse("Blog Posts page - Coming soon!")

def login_view(request):
    return HttpResponse("Login page - Coming soon!")

def register_view(request):
    return HttpResponse("Register page - Coming soon!")

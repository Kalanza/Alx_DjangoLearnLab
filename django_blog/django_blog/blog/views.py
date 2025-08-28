from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

# Create your views here.

def home(request):
    return render(request, 'blog/home.html')

def posts(request):
    return HttpResponse("Blog posts will be displayed here.")

def login_view(request):
    return HttpResponse("Login page - to be implemented.")

def register_view(request):
    return HttpResponse("Register page - to be implemented.")

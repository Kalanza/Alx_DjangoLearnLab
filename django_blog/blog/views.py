from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

# Create your views here.

def home(request):
    posts = Post.objects.all()[:5]  # Get the 5 most recent posts
    return render(request, 'blog/home.html', {'posts': posts})

def posts(request):
    return HttpResponse("Blog Posts page - Coming soon!")

def login_view(request):
    return HttpResponse("Login page - Coming soon!")

def register_view(request):
    return HttpResponse("Register page - Coming soon!")

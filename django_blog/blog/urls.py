from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home and blog posts
    path('', views.home, name='home'),
    path('posts/', views.posts_list, name='posts'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Profile management
    path('profile/', views.profile_view, name='profile'),
]

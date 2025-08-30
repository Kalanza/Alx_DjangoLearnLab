#!/usr/bin/env python
"""
This script creates sample blog posts for testing the Django blog application.
Run this script from the django_blog directory using: python create_sample_posts.py
"""

import os
import sys
import django

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
django.setup()

from blog.models import Post
from django.contrib.auth.models import User

def create_sample_posts():
    """Create sample blog posts for testing."""
    
    # Get or create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    # Sample posts data
    sample_posts = [
        {
            'title': 'Welcome to Our Django Blog',
            'content': '''Welcome to our brand new Django blog! This is our first post, and we're excited to share our journey with you. 
            
This blog will feature tutorials, tips, and insights about Django development, web programming, and software engineering best practices. 

We hope you'll find the content valuable and engaging. Stay tuned for more exciting posts!'''
        },
        {
            'title': 'Getting Started with Django Models',
            'content': '''Django models are the foundation of any Django application. They define the structure of your database and provide a high-level API for interacting with your data.

In this post, we'll explore how to create models, define relationships between them, and use Django's powerful ORM to query your data.

Key concepts we'll cover:
- Model fields and their types
- Relationships (ForeignKey, ManyToMany, OneToOne)
- Model methods and properties
- Database migrations'''
        },
        {
            'title': 'Django Templates and Static Files',
            'content': '''Templates are essential for creating dynamic web pages in Django. They allow you to separate your presentation logic from your business logic.

In this comprehensive guide, we'll learn about:
- Template syntax and variables
- Template inheritance and blocks
- Static files management
- CSS and JavaScript integration
- Best practices for organizing templates

Django's template system is powerful and flexible, making it easy to create maintainable and scalable web applications.'''
        }
    ]
    
    # Create posts
    for post_data in sample_posts:
        post, created = Post.objects.get_or_create(
            title=post_data['title'],
            defaults={
                'content': post_data['content'],
                'author': admin_user
            }
        )
        if created:
            print(f"Created post: {post.title}")
        else:
            print(f"Post already exists: {post.title}")
    
    print(f"\nTotal posts in database: {Post.objects.count()}")

if __name__ == '__main__':
    create_sample_posts()

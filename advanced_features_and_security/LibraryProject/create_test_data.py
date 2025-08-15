"""
Test script to create sample data and test users for the permissions system.
Run this with: python manage.py shell < create_test_data.py
"""

from django.contrib.auth.models import Group
from bookshelf.models import CustomUser, UserProfile, Book

# Create some sample books
books_data = [
    {"title": "Django for Beginners", "author": "William S. Vincent", "publication_year": 2022},
    {"title": "Two Scoops of Django", "author": "Daniel Roy Greenfeld", "publication_year": 2021},
    {"title": "Python Crash Course", "author": "Eric Matthes", "publication_year": 2023},
]

print("Creating sample books...")
for book_data in books_data:
    book, created = Book.objects.get_or_create(**book_data)
    if created:
        print(f"Created book: {book}")
    else:
        print(f"Book already exists: {book}")

# Create test users
users_data = [
    {"username": "viewer_user", "email": "viewer@example.com", "password": "testpass123", "group": "Viewers"},
    {"username": "editor_user", "email": "editor@example.com", "password": "testpass123", "group": "Editors"},
    {"username": "admin_user", "email": "admin@example.com", "password": "testpass123", "group": "Admins"},
]

print("\nCreating test users...")
for user_data in users_data:
    group_name = user_data.pop('group')
    password = user_data.pop('password')
    
    user, created = CustomUser.objects.get_or_create(
        username=user_data['username'],
        defaults=user_data
    )
    
    if created:
        user.set_password(password)
        user.save()
        
        # Add to group
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        
        print(f"Created user: {user.username} in group: {group_name}")
    else:
        print(f"User already exists: {user.username}")

print("\n" + "="*50)
print("TEST DATA CREATED SUCCESSFULLY!")
print("="*50)
print("\nTest Users Created:")
print("1. viewer_user (password: testpass123) - Can only view books")
print("2. editor_user (password: testpass123) - Can create and edit books")
print("3. admin_user (password: testpass123) - Full access to all operations")
print("\nAccess the application at:")
print("- Book list: http://127.0.0.1:8000/bookshelf/books/")
print("- Admin panel: http://127.0.0.1:8000/admin/")
print("\nTest the permissions by logging in as different users!")

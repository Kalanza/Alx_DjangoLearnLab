#!/usr/bin/env python
"""
Security setup and testing script for LibraryProject.
This script sets up users with appropriate permissions for testing security features.
"""
import os
import sys
import django

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from bookshelf.models import UserProfile, Book

User = get_user_model()

def setup_test_users_and_permissions():
    """
    Create test users with different permission levels for security testing.
    """
    print("Setting up security test users and permissions...")
    
    # Create groups
    admin_group, created = Group.objects.get_or_create(name='Admin')
    librarian_group, created = Group.objects.get_or_create(name='Librarian')
    member_group, created = Group.objects.get_or_create(name='Member')
    
    # Get book permissions
    permissions = {
        'can_view': Permission.objects.get(codename='can_view'),
        'can_create': Permission.objects.get(codename='can_create'),
        'can_edit': Permission.objects.get(codename='can_edit'),
        'can_delete': Permission.objects.get(codename='can_delete'),
    }
    
    # Assign permissions to groups
    admin_group.permissions.set(permissions.values())
    librarian_group.permissions.set([permissions['can_view'], permissions['can_create'], permissions['can_edit']])
    member_group.permissions.set([permissions['can_view']])
    
    # Create test users
    users_data = [
        {
            'username': 'security_admin',
            'email': 'admin@security-test.com',
            'password': 'SecureAdminPass123!',
            'group': admin_group,
            'role': 'Admin',
            'is_staff': True,
            'is_superuser': True
        },
        {
            'username': 'security_librarian',
            'email': 'librarian@security-test.com',
            'password': 'SecureLibrarianPass123!',
            'group': librarian_group,
            'role': 'Librarian',
            'is_staff': False,
            'is_superuser': False
        },
        {
            'username': 'security_member',
            'email': 'member@security-test.com',
            'password': 'SecureMemberPass123!',
            'group': member_group,
            'role': 'Member',
            'is_staff': False,
            'is_superuser': False
        },
        {
            'username': 'security_nogroup',
            'email': 'nogroup@security-test.com',
            'password': 'SecureNoGroupPass123!',
            'group': None,
            'role': 'Member',
            'is_staff': False,
            'is_superuser': False
        }
    ]
    
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'is_staff': user_data['is_staff'],
                'is_superuser': user_data['is_superuser']
            }
        )
        
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"Created user: {user.username}")
        else:
            print(f"User already exists: {user.username}")
        
        # Assign to group
        if user_data['group']:
            user.groups.add(user_data['group'])
        
        # Create or update user profile
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': user_data['role']}
        )
        if not created:
            profile.role = user_data['role']
            profile.save()
    
    print("User setup complete!")
    return users_data

def create_test_books():
    """
    Create some test books for security testing.
    """
    print("Creating test books...")
    
    test_books = [
        {
            'title': 'Security Fundamentals',
            'author': 'Security Expert',
            'publication_year': 2023
        },
        {
            'title': 'Web Application Security',
            'author': 'Cyber Security Pro',
            'publication_year': 2022
        },
        {
            'title': 'Django Security Best Practices',
            'author': 'Django Developer',
            'publication_year': 2024
        }
    ]
    
    for book_data in test_books:
        book, created = Book.objects.get_or_create(
            title=book_data['title'],
            defaults=book_data
        )
        if created:
            print(f"Created book: {book.title}")
        else:
            print(f"Book already exists: {book.title}")

def run_security_checks():
    """
    Run basic security validation checks.
    """
    print("\nRunning security validation checks...")
    
    # Check that users have correct permissions
    admin_user = User.objects.get(username='security_admin')
    librarian_user = User.objects.get(username='security_librarian')
    member_user = User.objects.get(username='security_member')
    
    print(f"Admin permissions: {list(admin_user.user_permissions.values_list('codename', flat=True))}")
    print(f"Librarian group permissions: {list(librarian_user.groups.first().permissions.values_list('codename', flat=True)) if librarian_user.groups.exists() else 'No groups'}")
    print(f"Member group permissions: {list(member_user.groups.first().permissions.values_list('codename', flat=True)) if member_user.groups.exists() else 'No groups'}")
    
    # Check book count
    book_count = Book.objects.count()
    print(f"Total books in database: {book_count}")
    
    print("\nSecurity setup validation complete!")

def print_security_testing_instructions():
    """
    Print instructions for manual security testing.
    """
    print("\n" + "="*60)
    print("SECURITY TESTING INSTRUCTIONS")
    print("="*60)
    print("\n1. CSRF PROTECTION TESTING:")
    print("   - Try submitting forms without CSRF tokens")
    print("   - Verify forms include {% csrf_token %}")
    
    print("\n2. XSS PROTECTION TESTING:")
    print("   - Try entering <script>alert('XSS')</script> in form fields")
    print("   - Verify input is rejected or escaped")
    
    print("\n3. SQL INJECTION TESTING:")
    print("   - Try entering SQL injection patterns in search:")
    print("     - '; DROP TABLE bookshelf_book; --")
    print("     - ' UNION SELECT * FROM users --")
    
    print("\n4. PERMISSION TESTING:")
    print("   Test with different user accounts:")
    print("   - security_admin (full permissions)")
    print("   - security_librarian (view, create, edit)")
    print("   - security_member (view only)")
    print("   - security_nogroup (no permissions)")
    
    print("\n5. SECURITY HEADERS TESTING:")
    print("   - Check browser developer tools for security headers")
    print("   - Verify CSP, X-Frame-Options, etc. are present")
    
    print("\n6. SESSION SECURITY:")
    print("   - Verify session cookies are httponly")
    print("   - Check session timeout behavior")
    
    print("\nTest Users Created:")
    print("-" * 30)
    users = User.objects.filter(username__startswith='security_')
    for user in users:
        groups = ", ".join([g.name for g in user.groups.all()]) if user.groups.exists() else "No groups"
        print(f"Username: {user.username}")
        print(f"Password: SecureAdminPass123! (or similar)")
        print(f"Groups: {groups}")
        print(f"Staff: {user.is_staff}, Superuser: {user.is_superuser}")
        print("-" * 30)

if __name__ == '__main__':
    print("LibraryProject Security Setup Script")
    print("====================================")
    
    try:
        # Setup users and permissions
        setup_test_users_and_permissions()
        
        # Create test data
        create_test_books()
        
        # Run validation checks
        run_security_checks()
        
        # Print testing instructions
        print_security_testing_instructions()
        
        print("\n✅ Security setup completed successfully!")
        print("\nYou can now:")
        print("1. Run the development server: python manage.py runserver")
        print("2. Run security tests: python manage.py test security_tests")
        print("3. Access admin panel: http://127.0.0.1:8000/admin/")
        print("4. Access book list: http://127.0.0.1:8000/bookshelf/books/")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        sys.exit(1)

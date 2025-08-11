#!/usr/bin/env python
"""
Script to test the role-based access control system
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User
from relationship_app.models import UserProfile
from relationship_app.views import is_admin, is_librarian, is_member

def test_role_system():
    """Test the role-based access control system"""
    print("=== Testing Role-Based Access Control System ===")
    
    # Get the first user
    user = User.objects.first()
    if not user:
        print("No users found in database")
        return
    
    print(f"\nTesting user: {user.username}")
    print(f"User authenticated: {user.is_authenticated}")
    print(f"Has UserProfile: {hasattr(user, 'userprofile')}")
    
    if hasattr(user, 'userprofile'):
        print(f"Current role: {user.userprofile.role}")
        
        print("\nTesting role check functions:")
        print(f"is_admin(user): {is_admin(user)}")
        print(f"is_librarian(user): {is_librarian(user)}")
        print(f"is_member(user): {is_member(user)}")
        
        print("\nTesting role changes:")
        original_role = user.userprofile.role
        
        # Test Admin role
        user.userprofile.role = UserProfile.ADMIN
        user.userprofile.save()
        print(f"Changed to Admin - is_admin: {is_admin(user)}")
        
        # Test Librarian role
        user.userprofile.role = UserProfile.LIBRARIAN
        user.userprofile.save()
        print(f"Changed to Librarian - is_librarian: {is_librarian(user)}")
        
        # Test Member role
        user.userprofile.role = UserProfile.MEMBER
        user.userprofile.save()
        print(f"Changed to Member - is_member: {is_member(user)}")
        
        # Restore original role
        user.userprofile.role = original_role
        user.userprofile.save()
        print(f"Restored original role: {original_role}")
        
    else:
        print("User doesn't have a UserProfile!")
    
    print("\n=== Test Complete ===")

if __name__ == '__main__':
    test_role_system()

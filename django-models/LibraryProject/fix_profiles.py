#!/usr/bin/env python
"""
Script to create UserProfile objects for existing users
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User
from relationship_app.models import UserProfile

def create_missing_profiles():
    """Create UserProfile objects for users who don't have them"""
    users_without_profiles = []
    
    for user in User.objects.all():
        if not hasattr(user, 'userprofile'):
            users_without_profiles.append(user)
    
    print(f"Found {len(users_without_profiles)} users without profiles")
    
    for user in users_without_profiles:
        # Create profile with default Member role
        profile = UserProfile.objects.create(
            user=user,
            role=UserProfile.MEMBER
        )
        print(f"Created profile for user: {user.username}")
    
    print("Done!")

if __name__ == '__main__':
    create_missing_profiles()

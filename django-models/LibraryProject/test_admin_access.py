#!/usr/bin/env python
"""
Detailed test for Admin Access Control
This script tests the specific admin view requirements
"""

import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from relationship_app.models import UserProfile
from relationship_app.admin_view import is_admin, admin_view

def test_admin_access_detailed():
    """Test Admin access control in detail"""
    
    print("=" * 70)
    print("DETAILED ADMIN ACCESS CONTROL TEST")
    print("=" * 70)
    
    # Clean up any existing test users
    User.objects.filter(username__startswith='test_admin').delete()
    User.objects.filter(username__startswith='test_member').delete()
    
    client = Client()
    
    print("\n1. TESTING ADMIN USER CREATION AND ROLE ASSIGNMENT:")
    print("-" * 60)
    
    # Create admin user
    admin_user = User.objects.create_user(
        username='test_admin_user', 
        password='testpass123',
        email='admin@test.com'
    )
    
    # Check if UserProfile was created automatically
    if hasattr(admin_user, 'userprofile'):
        print(f"✓ UserProfile automatically created for {admin_user.username}")
        print(f"  Default role: {admin_user.userprofile.role}")
    else:
        print(f"✗ UserProfile NOT created for {admin_user.username}")
        return False
    
    # Set admin role
    admin_user.userprofile.role = UserProfile.ADMIN
    admin_user.userprofile.save()
    admin_user.refresh_from_db()
    
    print(f"✓ Admin role assigned: {admin_user.userprofile.role}")
    print(f"✓ UserProfile.ADMIN constant: '{UserProfile.ADMIN}'")
    print(f"✓ Role matches constant: {admin_user.userprofile.role == UserProfile.ADMIN}")
    
    print("\n2. TESTING is_admin() FUNCTION:")
    print("-" * 60)
    
    # Test is_admin function
    result = is_admin(admin_user)
    print(f"✓ is_admin(admin_user): {result}")
    
    # Detailed breakdown
    print(f"  - user.is_authenticated: {admin_user.is_authenticated}")
    print(f"  - hasattr(user, 'userprofile'): {hasattr(admin_user, 'userprofile')}")
    if hasattr(admin_user, 'userprofile'):
        print(f"  - user.userprofile.role: '{admin_user.userprofile.role}'")
        print(f"  - UserProfile.ADMIN: '{UserProfile.ADMIN}'")
        print(f"  - role == ADMIN: {admin_user.userprofile.role == UserProfile.ADMIN}")
    
    if not result:
        print("✗ is_admin() function failed!")
        return False
    
    print("\n3. TESTING NON-ADMIN USER:")
    print("-" * 60)
    
    # Create member user
    member_user = User.objects.create_user(
        username='test_member_user',
        password='testpass123'
    )
    
    # Member should have default role (Member)
    print(f"✓ Member user created with role: {member_user.userprofile.role}")
    
    # Test is_admin with member user
    member_result = is_admin(member_user)
    print(f"✓ is_admin(member_user): {member_result}")
    
    if member_result:
        print("✗ is_admin() incorrectly returned True for member user!")
        return False
    
    print("\n4. TESTING UNAUTHENTICATED ACCESS:")
    print("-" * 60)
    
    # Test without login
    response = client.get(reverse('admin_dashboard'))
    print(f"✓ Unauthenticated access status: {response.status_code}")
    print(f"✓ Expected redirect (302): {response.status_code == 302}")
    
    if response.status_code != 302:
        print("✗ Unauthenticated users should be redirected!")
        return False
    
    print("\n5. TESTING MEMBER USER ACCESS (SHOULD BE DENIED):")
    print("-" * 60)
    
    # Login as member
    login_success = client.login(username='test_member_user', password='testpass123')
    print(f"✓ Member login successful: {login_success}")
    
    if login_success:
        response = client.get(reverse('admin_dashboard'))
        print(f"✓ Member access to admin dashboard status: {response.status_code}")
        print(f"✓ Expected denial/redirect (302): {response.status_code == 302}")
        
        if response.status_code != 302:
            print("✗ Member users should be denied access to admin dashboard!")
            return False
    
    client.logout()
    
    print("\n6. TESTING ADMIN USER ACCESS (SHOULD BE ALLOWED):")
    print("-" * 60)
    
    # Login as admin
    login_success = client.login(username='test_admin_user', password='testpass123')
    print(f"✓ Admin login successful: {login_success}")
    
    if login_success:
        response = client.get(reverse('admin_dashboard'))
        print(f"✓ Admin access to admin dashboard status: {response.status_code}")
        print(f"✓ Expected success (200): {response.status_code == 200}")
        
        if response.status_code != 200:
            print("✗ Admin users should be able to access admin dashboard!")
            print(f"Response content preview: {response.content[:200].decode('utf-8', errors='ignore')}")
            return False
            
        # Check if response contains admin content
        content = response.content.decode('utf-8')
        if "Admin Dashboard" in content and admin_user.username in content:
            print("✓ Admin dashboard content is correct")
        else:
            print("✗ Admin dashboard content is missing or incorrect")
            return False
    
    print("\n7. TESTING URL PATTERN:")
    print("-" * 60)
    
    try:
        admin_url = reverse('admin_dashboard')
        print(f"✓ Admin dashboard URL: {admin_url}")
        print(f"✓ URL reversal successful")
    except Exception as e:
        print(f"✗ URL reversal failed: {e}")
        return False
    
    print("\n8. TESTING TEMPLATE:")
    print("-" * 60)
    
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'admin_view.html')
    if os.path.exists(template_path):
        print(f"✓ Admin template exists at: {template_path}")
        
        # Check template content
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
            if "Admin Dashboard" in template_content and "{{ user.username }}" in template_content:
                print("✓ Template contains required admin content")
            else:
                print("✗ Template missing required content")
                return False
    else:
        print(f"✗ Admin template not found at: {template_path}")
        return False
    
    # Cleanup
    admin_user.delete()
    member_user.delete()
    
    print("\n" + "=" * 70)
    print("✅ ALL ADMIN ACCESS CONTROL TESTS PASSED!")
    print("The Admin view implementation is correct and working properly.")
    print("=" * 70)
    
    return True

if __name__ == '__main__':
    try:
        success = test_admin_access_detailed()
        if success:
            print("\n🎉 Your Admin access control is working perfectly!")
            print("The implementation meets all requirements.")
        else:
            print("\n⚠️  There are issues with the Admin access control.")
            print("Please review the failed tests above.")
    except Exception as e:
        print(f"\n💥 Test failed with exception: {e}")
        import traceback
        traceback.print_exc()

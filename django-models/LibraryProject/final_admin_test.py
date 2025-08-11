#!/usr/bin/env python
"""
Final comprehensive test for Admin View requirements
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
from relationship_app import views

def test_admin_requirements():
    """Test all admin view requirements"""
    
    print("=" * 60)
    print("COMPREHENSIVE ADMIN VIEW REQUIREMENTS TEST")
    print("=" * 60)
    
    # Clean up any existing test users
    User.objects.filter(username__startswith='test_').delete()
    
    results = []
    
    print("\n1. CHECKING ADMIN VIEW FUNCTION EXISTS:")
    print("-" * 50)
    
    if hasattr(views, 'admin_view'):
        print("✅ admin_view function exists in views.py")
        results.append(True)
    else:
        print("❌ admin_view function NOT found in views.py")
        results.append(False)
    
    print("\n2. CHECKING USER_PASSES_TEST DECORATOR:")
    print("-" * 50)
    
    # Check if admin_view has the decorator
    if hasattr(views.admin_view, '__wrapped__'):
        print("✅ admin_view has decorator applied")
        results.append(True)
    else:
        print("❌ admin_view missing @user_passes_test decorator")
        results.append(False)
    
    print("\n3. CHECKING is_admin FUNCTION:")
    print("-" * 50)
    
    if hasattr(views, 'is_admin'):
        print("✅ is_admin function exists")
        
        # Create test users
        admin_user = User.objects.create_user('test_admin', 'admin@test.com', 'pass123')
        admin_user.userprofile.role = UserProfile.ADMIN
        admin_user.userprofile.save()
        
        member_user = User.objects.create_user('test_member', 'member@test.com', 'pass123')
        # member_user keeps default Member role
        
        # Test is_admin function
        admin_check = views.is_admin(admin_user)
        member_check = views.is_admin(member_user)
        
        if admin_check and not member_check:
            print("✅ is_admin function works correctly")
            print(f"   - Admin user: {admin_check}")
            print(f"   - Member user: {member_check}")
            results.append(True)
        else:
            print("❌ is_admin function not working correctly")
            print(f"   - Admin user: {admin_check} (should be True)")
            print(f"   - Member user: {member_check} (should be False)")
            results.append(False)
            
        # Clean up
        admin_user.delete()
        member_user.delete()
    else:
        print("❌ is_admin function NOT found")
        results.append(False)
    
    print("\n4. TESTING ACCESS CONTROL:")
    print("-" * 50)
    
    client = Client()
    
    # Create admin and member users
    admin_user = User.objects.create_user('test_admin2', 'admin@test.com', 'pass123')
    admin_user.userprofile.role = UserProfile.ADMIN
    admin_user.userprofile.save()
    
    member_user = User.objects.create_user('test_member2', 'member@test.com', 'pass123')
    
    # Test 1: Unauthenticated access
    response = client.get(reverse('admin_dashboard'))
    if response.status_code == 302:
        print("✅ Unauthenticated users are redirected")
        results.append(True)
    else:
        print(f"❌ Unauthenticated access returned {response.status_code}, expected 302")
        results.append(False)
    
    # Test 2: Member access (should be denied)
    client.login(username='test_member2', password='pass123')
    response = client.get(reverse('admin_dashboard'))
    if response.status_code == 302:
        print("✅ Member users are denied access")
        results.append(True)
    else:
        print(f"❌ Member access returned {response.status_code}, expected 302")
        results.append(False)
    client.logout()
    
    # Test 3: Admin access (should be allowed)
    client.login(username='test_admin2', password='pass123')
    response = client.get(reverse('admin_dashboard'))
    if response.status_code == 200:
        print("✅ Admin users can access the view")
        results.append(True)
    else:
        print(f"❌ Admin access returned {response.status_code}, expected 200")
        results.append(False)
    
    # Clean up
    admin_user.delete()
    member_user.delete()
    
    print("\n5. CHECKING URL CONFIGURATION:")
    print("-" * 50)
    
    try:
        admin_url = reverse('admin_dashboard')
        if '/admin_dashboard/' in admin_url:
            print("✅ Admin dashboard URL is properly configured")
            print(f"   URL: {admin_url}")
            results.append(True)
        else:
            print(f"❌ Admin dashboard URL incorrect: {admin_url}")
            results.append(False)
    except Exception as e:
        print(f"❌ Admin dashboard URL not found: {e}")
        results.append(False)
    
    print("\n6. CHECKING TEMPLATE:")
    print("-" * 50)
    
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'admin_view.html')
    if os.path.exists(template_path):
        print("✅ admin_view.html template exists")
        results.append(True)
    else:
        print("❌ admin_view.html template not found")
        results.append(False)
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 ALL ADMIN VIEW REQUIREMENTS SATISFIED!")
        print(f"Score: {passed}/{total} (100%)")
        print("\nYour admin view implementation is COMPLETE and CORRECT!")
        print("It should pass all automated tests.")
    else:
        print(f"⚠️  SOME REQUIREMENTS NOT MET: {passed}/{total}")
        print("\nPlease review the failed checks above.")
    
    print("=" * 60)
    
    return passed == total

if __name__ == '__main__':
    test_admin_requirements()

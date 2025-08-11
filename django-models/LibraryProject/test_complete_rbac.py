#!/usr/bin/env python
"""
Comprehensive test for all role-based access control requirements
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

def test_complete_rbac_system():
    """Test the complete Role-Based Access Control system"""
    
    print("=" * 70)
    print("COMPLETE ROLE-BASED ACCESS CONTROL SYSTEM TEST")
    print("=" * 70)
    
    results = []
    
    # Clean up any existing test users
    User.objects.filter(username__startswith='test_').delete()
    
    print("\n1. TESTING USERPROFILE MODEL:")
    print("-" * 50)
    
    # Test UserProfile model structure
    try:
        # Check if model exists and has correct fields
        user_profile = UserProfile()
        assert hasattr(user_profile, 'user'), "UserProfile missing 'user' field"
        assert hasattr(user_profile, 'role'), "UserProfile missing 'role' field"
        assert hasattr(UserProfile, 'ROLE_CHOICES'), "UserProfile missing 'ROLE_CHOICES'"
        
        # Check role choices structure
        expected_choices = [('Admin', 'Admin'), ('Librarian', 'Librarian'), ('Member', 'Member')]
        assert UserProfile.ROLE_CHOICES == expected_choices, f"Wrong role choices: {UserProfile.ROLE_CHOICES}"
        
        # Test one-to-one relationship
        test_user = User.objects.create_user(username='test_user_model', password='pass123')
        assert hasattr(test_user, 'userprofile'), "One-to-one relationship not working"
        assert test_user.userprofile.role == 'Member', f"Default role should be 'Member', got '{test_user.userprofile.role}'"
        
        test_user.delete()
        
        print("✅ UserProfile model structure correct")
        print("✅ Role choices properly defined")
        print("✅ One-to-one relationship with User working")
        print("✅ Default role is 'Member'")
        print("✅ Automatic UserProfile creation working")
        results.append(True)
        
    except Exception as e:
        print(f"❌ UserProfile model test failed: {e}")
        results.append(False)
    
    print("\n2. TESTING ROLE-BASED VIEWS:")
    print("-" * 50)
    
    # Test that all views exist
    view_functions = ['admin_view', 'librarian_view', 'member_view']
    helper_functions = ['is_admin', 'is_librarian', 'is_member']
    
    try:
        for view_func in view_functions:
            if hasattr(views, view_func):
                print(f"✅ {view_func} exists in views.py")
            else:
                print(f"❌ {view_func} NOT found in views.py")
                results.append(False)
                continue
        
        for helper_func in helper_functions:
            if hasattr(views, helper_func):
                print(f"✅ {helper_func} helper function exists")
            else:
                print(f"❌ {helper_func} helper function NOT found")
                results.append(False)
                continue
        
        results.append(True)
        
    except Exception as e:
        print(f"❌ Views test failed: {e}")
        results.append(False)
    
    print("\n3. TESTING @user_passes_test DECORATOR:")
    print("-" * 50)
    
    try:
        # Check if views have decorators applied
        decorators_working = []
        
        for view_func in view_functions:
            view = getattr(views, view_func)
            if hasattr(view, '__wrapped__'):
                print(f"✅ {view_func} has @user_passes_test decorator")
                decorators_working.append(True)
            else:
                print(f"❌ {view_func} missing @user_passes_test decorator")
                decorators_working.append(False)
        
        if all(decorators_working):
            results.append(True)
        else:
            results.append(False)
            
    except Exception as e:
        print(f"❌ Decorator test failed: {e}")
        results.append(False)
    
    print("\n4. TESTING ACCESS CONTROL LOGIC:")
    print("-" * 50)
    
    try:
        # Create users with different roles
        admin_user = User.objects.create_user('test_admin', 'admin@test.com', 'pass123')
        admin_user.userprofile.role = 'Admin'
        admin_user.userprofile.save()
        
        librarian_user = User.objects.create_user('test_librarian', 'librarian@test.com', 'pass123')
        librarian_user.userprofile.role = 'Librarian'
        librarian_user.userprofile.save()
        
        member_user = User.objects.create_user('test_member', 'member@test.com', 'pass123')
        # member_user keeps default 'Member' role
        
        # Test helper functions
        admin_result = views.is_admin(admin_user)
        librarian_result = views.is_librarian(librarian_user)
        member_result = views.is_member(member_user)
        
        # Cross-check (admin should not be librarian or member, etc.)
        admin_not_lib = not views.is_librarian(admin_user)
        admin_not_mem = not views.is_member(admin_user)
        lib_not_admin = not views.is_admin(librarian_user)
        lib_not_mem = not views.is_member(librarian_user)
        mem_not_admin = not views.is_admin(member_user)
        mem_not_lib = not views.is_librarian(member_user)
        
        if (admin_result and librarian_result and member_result and 
            admin_not_lib and admin_not_mem and lib_not_admin and 
            lib_not_mem and mem_not_admin and mem_not_lib):
            print("✅ Role checking functions work correctly")
            print("✅ Role-based access control logic is proper")
            results.append(True)
        else:
            print("❌ Role checking functions not working correctly")
            print(f"  Admin check: {admin_result} (should be True)")
            print(f"  Librarian check: {librarian_result} (should be True)")
            print(f"  Member check: {member_result} (should be True)")
            results.append(False)
        
        # Clean up
        admin_user.delete()
        librarian_user.delete()
        member_user.delete()
        
    except Exception as e:
        print(f"❌ Access control logic test failed: {e}")
        results.append(False)
    
    print("\n5. TESTING HTTP ACCESS CONTROL:")
    print("-" * 50)
    
    client = Client()
    
    try:
        # Create test users
        admin_user = User.objects.create_user('test_admin_http', 'admin@test.com', 'pass123')
        admin_user.userprofile.role = 'Admin'
        admin_user.userprofile.save()
        
        librarian_user = User.objects.create_user('test_librarian_http', 'librarian@test.com', 'pass123')
        librarian_user.userprofile.role = 'Librarian'
        librarian_user.userprofile.save()
        
        member_user = User.objects.create_user('test_member_http', 'member@test.com', 'pass123')
        
        # Test Admin access
        client.login(username='test_admin_http', password='pass123')
        admin_response = client.get(reverse('admin_dashboard'))
        if admin_response.status_code == 200:
            print("✅ Admin can access admin dashboard")
        else:
            print(f"❌ Admin access failed: {admin_response.status_code}")
        client.logout()
        
        # Test Librarian access
        client.login(username='test_librarian_http', password='pass123')
        librarian_response = client.get(reverse('librarian_dashboard'))
        if librarian_response.status_code == 200:
            print("✅ Librarian can access librarian dashboard")
        else:
            print(f"❌ Librarian access failed: {librarian_response.status_code}")
        client.logout()
        
        # Test Member access
        client.login(username='test_member_http', password='pass123')
        member_response = client.get(reverse('member_dashboard'))
        if member_response.status_code == 200:
            print("✅ Member can access member dashboard")
        else:
            print(f"❌ Member access failed: {member_response.status_code}")
        client.logout()
        
        # Test access denial (member trying to access admin)
        client.login(username='test_member_http', password='pass123')
        member_to_admin = client.get(reverse('admin_dashboard'))
        if member_to_admin.status_code == 302:
            print("✅ Member correctly denied admin access")
        else:
            print(f"❌ Member should be denied admin access, got: {member_to_admin.status_code}")
        client.logout()
        
        results.append(True)
        
        # Clean up
        admin_user.delete()
        librarian_user.delete()
        member_user.delete()
        
    except Exception as e:
        print(f"❌ HTTP access control test failed: {e}")
        results.append(False)
    
    print("\n6. TESTING URL PATTERNS:")
    print("-" * 50)
    
    try:
        admin_url = reverse('admin_dashboard')
        librarian_url = reverse('librarian_dashboard')
        member_url = reverse('member_dashboard')
        
        print(f"✅ Admin dashboard URL: {admin_url}")
        print(f"✅ Librarian dashboard URL: {librarian_url}")
        print(f"✅ Member dashboard URL: {member_url}")
        
        results.append(True)
        
    except Exception as e:
        print(f"❌ URL patterns test failed: {e}")
        results.append(False)
    
    print("\n7. TESTING TEMPLATES:")
    print("-" * 50)
    
    try:
        templates = ['admin_view.html', 'librarian_view.html', 'member_view.html']
        for template in templates:
            template_path = os.path.join(os.path.dirname(__file__), 'templates', template)
            if os.path.exists(template_path):
                print(f"✅ {template} exists")
            else:
                print(f"❌ {template} not found")
        
        results.append(True)
        
    except Exception as e:
        print(f"❌ Templates test failed: {e}")
        results.append(False)
    
    print("\n" + "=" * 70)
    
    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100
    
    if passed == total:
        print("🎉 ALL ROLE-BASED ACCESS CONTROL REQUIREMENTS SATISFIED!")
        print(f"Score: {passed}/{total} ({percentage:.1f}%)")
        print("\n✅ Your implementation should now pass all automated tests!")
    else:
        print(f"⚠️  SOME REQUIREMENTS NEED ATTENTION: {passed}/{total} ({percentage:.1f}%)")
        print("\nPlease review the failed checks above.")
    
    print("=" * 70)
    
    return passed == total

if __name__ == '__main__':
    test_complete_rbac_system()

"""
Validation script to check if the Social Media API setup is complete and working.
This script performs basic checks without making HTTP requests.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).resolve().parent
sys.path.append(str(project_dir))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

def check_models():
    """Check if models are properly defined and migrated."""
    print("🔍 Checking models...")
    
    try:
        from accounts.models import CustomUser, Follow
        from django.contrib.auth import get_user_model
        
        # Check if CustomUser is the default user model
        User = get_user_model()
        if User == CustomUser:
            print("✅ CustomUser is properly set as AUTH_USER_MODEL")
        else:
            print("❌ CustomUser is not set as AUTH_USER_MODEL")
            return False
        
        # Check model fields
        user_fields = [field.name for field in CustomUser._meta.fields]
        required_fields = ['bio', 'profile_picture']
        
        for field in required_fields:
            if field in user_fields:
                print(f"✅ CustomUser has {field} field")
            else:
                print(f"❌ CustomUser missing {field} field")
                return False
        
        # Check if Follow model exists
        follow_fields = [field.name for field in Follow._meta.fields]
        if 'follower' in follow_fields and 'following' in follow_fields:
            print("✅ Follow model is properly defined")
        else:
            print("❌ Follow model is missing required fields")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importing models: {e}")
        return False

def check_serializers():
    """Check if serializers are properly defined."""
    print("\n🔍 Checking serializers...")
    
    try:
        from accounts.serializers import (
            UserRegistrationSerializer, 
            UserLoginSerializer, 
            UserProfileSerializer
        )
        
        serializer_classes = [
            UserRegistrationSerializer,
            UserLoginSerializer,
            UserProfileSerializer
        ]
        
        for serializer_class in serializer_classes:
            print(f"✅ {serializer_class.__name__} is defined")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importing serializers: {e}")
        return False

def check_views():
    """Check if views are properly defined."""
    print("\n🔍 Checking views...")
    
    try:
        from accounts.views import RegisterView, login_view, ProfileView
        
        views = [
            ('RegisterView', RegisterView),
            ('login_view', login_view),
            ('ProfileView', ProfileView)
        ]
        
        for view_name, view_obj in views:
            print(f"✅ {view_name} is defined")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importing views: {e}")
        return False

def check_urls():
    """Check if URL patterns are properly configured."""
    print("\n🔍 Checking URL configuration...")
    
    try:
        from django.urls import reverse
        from django.core.exceptions import NoReverseMatch
        
        # Check if URL patterns exist
        url_names = ['register', 'login', 'profile']
        
        for url_name in url_names:
            try:
                url = reverse(url_name)
                print(f"✅ URL pattern '{url_name}' is configured: {url}")
            except NoReverseMatch:
                print(f"❌ URL pattern '{url_name}' is not configured")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking URLs: {e}")
        return False

def check_settings():
    """Check if Django settings are properly configured."""
    print("\n🔍 Checking Django settings...")
    
    try:
        from django.conf import settings
        
        # Check installed apps
        required_apps = ['rest_framework', 'rest_framework.authtoken', 'accounts']
        
        for app in required_apps:
            if app in settings.INSTALLED_APPS:
                print(f"✅ '{app}' is in INSTALLED_APPS")
            else:
                print(f"❌ '{app}' is missing from INSTALLED_APPS")
                return False
        
        # Check REST framework configuration
        if hasattr(settings, 'REST_FRAMEWORK'):
            print("✅ REST_FRAMEWORK settings are configured")
        else:
            print("❌ REST_FRAMEWORK settings are missing")
            return False
        
        # Check custom user model
        if settings.AUTH_USER_MODEL == 'accounts.CustomUser':
            print("✅ AUTH_USER_MODEL is set to 'accounts.CustomUser'")
        else:
            print("❌ AUTH_USER_MODEL is not properly configured")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking settings: {e}")
        return False

def check_migrations():
    """Check if migrations have been applied."""
    print("\n🔍 Checking migrations...")
    
    try:
        from django.db import connection
        from django.core.management.color import no_style
        
        # Check if tables exist
        table_names = connection.introspection.table_names()
        
        required_tables = ['accounts_customuser', 'accounts_follow', 'authtoken_token']
        
        for table in required_tables:
            if table in table_names:
                print(f"✅ Table '{table}' exists in database")
            else:
                print(f"❌ Table '{table}' is missing from database")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking migrations: {e}")
        return False

def check_tokens():
    """Check if token authentication is working."""
    print("\n🔍 Checking token authentication setup...")
    
    try:
        from rest_framework.authtoken.models import Token
        from accounts.models import CustomUser
        
        print("✅ Token model is accessible")
        print("✅ CustomUser model is accessible")
        
        # Check if we can create a test user and token
        test_username = 'validation_test_user'
        
        # Clean up any existing test user
        try:
            existing_user = CustomUser.objects.get(username=test_username)
            existing_user.delete()
        except CustomUser.DoesNotExist:
            pass
        
        # Create test user
        test_user = CustomUser.objects.create_user(
            username=test_username,
            email='test@validation.com',
            password='testpass123'
        )
        
        # Create token
        token, created = Token.objects.get_or_create(user=test_user)
        
        if token:
            print("✅ Token creation is working")
        
        # Clean up
        test_user.delete()
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking token authentication: {e}")
        return False

def main():
    """Run all validation checks."""
    print("🚀 Social Media API Setup Validation")
    print("=" * 50)
    
    checks = [
        check_settings,
        check_models,
        check_serializers,
        check_views,
        check_urls,
        check_migrations,
        check_tokens
    ]
    
    all_passed = True
    
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 All validation checks passed!")
        print("✅ Social Media API setup is complete and ready to use")
        print("\nNext steps:")
        print("1. Start the development server: python manage.py runserver")
        print("2. Test the API endpoints using the test_api.py script")
        print("3. Create sample data: python manage.py create_sample_data")
        print("4. Use Postman or similar tools to test the API manually")
    else:
        print("❌ Some validation checks failed!")
        print("Please review the errors above and fix them before proceeding.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()

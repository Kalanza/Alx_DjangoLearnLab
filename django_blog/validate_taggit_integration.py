#!/usr/bin/env python3
"""
Django-Taggit Integration Validation Script
This script validates that django-taggit is properly integrated into the Django blog project.
"""

import os
import re

def check_settings():
    """Check if taggit is in INSTALLED_APPS"""
    print("1. Checking settings.py...")
    try:
        with open('django_blog/settings.py', 'r') as f:
            content = f.read()
            if '"taggit"' in content or "'taggit'" in content:
                print("   ✅ 'taggit' found in INSTALLED_APPS")
                return True
            else:
                print("   ❌ 'taggit' NOT found in INSTALLED_APPS")
                return False
    except FileNotFoundError:
        print("   ❌ settings.py not found")
        return False

def check_models():
    """Check if TaggableManager is used in models"""
    print("2. Checking models.py...")
    try:
        with open('blog/models.py', 'r') as f:
            content = f.read()
            if 'TaggableManager' in content:
                print("   ✅ TaggableManager found in models.py")
                return True
            else:
                print("   ❌ TaggableManager NOT found in models.py")
                return False
    except FileNotFoundError:
        print("   ❌ models.py not found")
        return False

def check_forms():
    """Check if TagWidget is used in forms"""
    print("3. Checking forms.py...")
    try:
        with open('blog/forms.py', 'r') as f:
            content = f.read()
            if 'TagWidget' in content:
                print("   ✅ TagWidget found in forms.py")
                return True
            else:
                print("   ❌ TagWidget NOT found in forms.py")
                return False
    except FileNotFoundError:
        print("   ❌ forms.py not found")
        return False

def check_views():
    """Check if taggit models are imported in views"""
    print("4. Checking views.py...")
    try:
        with open('blog/views.py', 'r') as f:
            content = f.read()
            if 'from taggit.models import Tag' in content:
                print("   ✅ taggit Tag model imported in views.py")
                return True
            else:
                print("   ❌ taggit Tag model NOT imported in views.py")
                return False
    except FileNotFoundError:
        print("   ❌ views.py not found")
        return False

def main():
    """Run all validation checks"""
    print("Django-Taggit Integration Validation")
    print("=" * 40)
    
    checks = [
        check_settings,
        check_models,
        check_forms,
        check_views
    ]
    
    results = []
    for check in checks:
        results.append(check())
    
    print("\n" + "=" * 40)
    print("VALIDATION SUMMARY")
    print("=" * 40)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Checks passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL CHECKS PASSED! Django-taggit is properly integrated.")
        print("\nNext steps:")
        print("1. Run: python manage.py makemigrations")
        print("2. Run: python manage.py migrate")
        print("3. Test the functionality")
    else:
        print("⚠️  Some checks failed. Please review the implementation.")
    
    return passed == total

if __name__ == '__main__':
    main()

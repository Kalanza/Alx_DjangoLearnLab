#!/usr/bin/env python
"""
Final Static Files Verification Script
=====================================
This script performs comprehensive checks to verify static files implementation
for the Django blog authentication system.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
django.setup()

from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.template.loader import get_template
import re

def check_mark(condition, message):
    """Print a check mark or X based on condition"""
    symbol = "✅" if condition else "❌"
    print(f"{symbol} {message}")
    return condition

def main():
    print("🔍 FINAL STATIC FILES VERIFICATION")
    print("=" * 50)
    
    all_checks_passed = True
    
    # 1. Check Django Settings
    print("\n1️⃣ DJANGO SETTINGS CHECK")
    print("-" * 30)
    
    check1 = check_mark(
        hasattr(settings, 'STATIC_URL') and settings.STATIC_URL,
        f"STATIC_URL configured: {getattr(settings, 'STATIC_URL', 'NOT SET')}"
    )
    
    check2 = check_mark(
        hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS,
        f"STATICFILES_DIRS configured: {getattr(settings, 'STATICFILES_DIRS', 'NOT SET')}"
    )
    
    check3 = check_mark(
        'django.contrib.staticfiles' in settings.INSTALLED_APPS,
        "django.contrib.staticfiles in INSTALLED_APPS"
    )
    
    all_checks_passed &= check1 and check2 and check3
    
    # 2. Check File Existence
    print("\n2️⃣ STATIC FILES EXISTENCE CHECK")
    print("-" * 35)
    
    required_files = [
        'css/login_form.css',
        'css/register_form.css',
        'css/login.css',
        'css/register.css',
        'js/login.js', 
        'js/register.js'
    ]
    
    files_found = {}
    for file_path in required_files:
        found_path = find(file_path)
        files_found[file_path] = found_path
        check4 = check_mark(
            found_path is not None,
            f"Found {file_path}: {found_path if found_path else 'NOT FOUND'}"
        )
        all_checks_passed &= check4
    
    # 3. Check File Content
    print("\n3️⃣ STATIC FILES CONTENT CHECK") 
    print("-" * 34)
    
    # Check login_form.css content
    login_form_path = files_found.get('css/login_form.css')
    if login_form_path:
        try:
            with open(login_form_path, 'r', encoding='utf-8') as f:
                login_content = f.read()
            check5 = check_mark(
                '.login-form' in login_content,
                "login_form.css contains .login-form class"
            )
            check6 = check_mark(
                len(login_content.strip()) > 0,
                f"login_form.css is not empty ({len(login_content)} chars)"
            )
            all_checks_passed &= check5 and check6
        except Exception as e:
            check_mark(False, f"Error reading login_form.css: {e}")
            all_checks_passed = False
    
    # Check register_form.css content
    register_form_path = files_found.get('css/register_form.css')
    if register_form_path:
        try:
            with open(register_form_path, 'r', encoding='utf-8') as f:
                register_content = f.read()
            check7 = check_mark(
                '.register-form' in register_content,
                "register_form.css contains .register-form class"
            )
            check8 = check_mark(
                len(register_content.strip()) > 0,
                f"register_form.css is not empty ({len(register_content)} chars)"
            )
            all_checks_passed &= check7 and check8
        except Exception as e:
            check_mark(False, f"Error reading register_form.css: {e}")
            all_checks_passed = False
    
    # 4. Check Template References
    print("\n4️⃣ TEMPLATE REFERENCES CHECK")
    print("-" * 33)
    
    try:
        # Check login template
        login_template = get_template('registration/login.html')
        login_source = login_template.template.source
        
        check9 = check_mark(
            "{% load static %}" in login_source,
            "Login template loads static tags"
        )
        
        check10 = check_mark(
            "login_form.css" in login_source,
            "Login template references login_form.css"
        )
        
        all_checks_passed &= check9 and check10
        
    except Exception as e:
        check_mark(False, f"Error checking login template: {e}")
        all_checks_passed = False
    
    try:
        # Check register template  
        register_template = get_template('registration/register.html')
        register_source = register_template.template.source
        
        check11 = check_mark(
            "{% load static %}" in register_source,
            "Register template loads static tags"
        )
        
        check12 = check_mark(
            "register_form.css" in register_source,
            "Register template references register_form.css"
        )
        
        all_checks_passed &= check11 and check12
        
    except Exception as e:
        check_mark(False, f"Error checking register template: {e}")
        all_checks_passed = False
    
    # 5. Directory Structure Check
    print("\n5️⃣ DIRECTORY STRUCTURE CHECK")
    print("-" * 32)
    
    expected_dirs = [
        project_root / "static" / "css",
        project_root / "static" / "js", 
        project_root / "blog" / "static" / "css",
        project_root / "blog" / "static" / "js"
    ]
    
    for dir_path in expected_dirs:
        check13 = check_mark(
            dir_path.exists(),
            f"Directory exists: {dir_path}"
        )
        all_checks_passed &= check13
    
    # 6. Files in Multiple Locations Check
    print("\n6️⃣ MULTIPLE LOCATIONS CHECK")
    print("-" * 31)
    
    for file_name in ['login_form.css', 'register_form.css']:
        project_static = project_root / "static" / "css" / file_name
        app_static = project_root / "blog" / "static" / "css" / file_name
        
        check14 = check_mark(
            project_static.exists(),
            f"{file_name} exists in project static: {project_static}"
        )
        
        check15 = check_mark(
            app_static.exists(),
            f"{file_name} exists in app static: {app_static}"
        )
        
        all_checks_passed &= check14 and check15
    
    # Final Summary
    print("\n" + "=" * 50)
    if all_checks_passed:
        print("🎉 ALL STATIC FILES CHECKS PASSED!")
        print("✅ The implementation should meet automated check requirements.")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print("❌ Review the failed items above and fix them.")
    
    print("\n📊 SUMMARY:")
    print(f"   • Static files are {'✅ PROPERLY' if all_checks_passed else '❌ NOT PROPERLY'} configured")
    print(f"   • Templates are {'✅ CORRECTLY' if all_checks_passed else '❌ INCORRECTLY'} referencing static files")
    print(f"   • Directory structure is {'✅ CORRECT' if all_checks_passed else '❌ INCORRECT'}")
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

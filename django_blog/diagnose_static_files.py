#!/usr/bin/env python
"""
Diagnostic script to check static files implementation for login and register
"""

import os
import sys
import django
from pathlib import Path

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    django.setup()
    from django.conf import settings
    from django.contrib.staticfiles import finders
    from django.template.loader import get_template
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    sys.exit(1)

def check_static_files():
    """Check static files implementation"""
    print("🔍 STATIC FILES DIAGNOSTIC REPORT")
    print("=" * 50)
    
    issues = []
    success = []
    
    # 1. Check Django settings
    print("\n1. DJANGO SETTINGS CHECK:")
    try:
        print(f"   STATIC_URL: {settings.STATIC_URL}")
        print(f"   STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
        if hasattr(settings, 'STATIC_ROOT'):
            print(f"   STATIC_ROOT: {settings.STATIC_ROOT}")
        success.append("Django settings configured")
    except Exception as e:
        issues.append(f"Django settings error: {e}")
    
    # 2. Check file existence
    print("\n2. FILE EXISTENCE CHECK:")
    static_files = [
        'blog/static/css/login.css',
        'blog/static/css/register.css', 
        'blog/static/js/login.js',
        'blog/static/js/register.js',
        'static/css/login.css',
        'static/css/register.css',
        'static/js/login.js',
        'static/js/register.js'
    ]
    
    for file_path in static_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
            success.append(f"File exists: {file_path}")
        else:
            print(f"   ❌ {file_path}")
            issues.append(f"Missing file: {file_path}")
    
    # 3. Check Django staticfiles finder
    print("\n3. DJANGO STATICFILES FINDER CHECK:")
    finder_files = [
        'css/login.css',
        'css/register.css',
        'js/login.js', 
        'js/register.js'
    ]
    
    for file_path in finder_files:
        try:
            found = finders.find(file_path)
            if found:
                print(f"   ✅ Django can find: {file_path} -> {found}")
                success.append(f"Django finder: {file_path}")
            else:
                print(f"   ❌ Django cannot find: {file_path}")
                issues.append(f"Django finder failed: {file_path}")
        except Exception as e:
            print(f"   ❌ Error finding {file_path}: {e}")
            issues.append(f"Finder error for {file_path}: {e}")
    
    # 4. Check template references
    print("\n4. TEMPLATE STATIC REFERENCES CHECK:")
    templates = [
        'registration/login.html',
        'registration/register.html'
    ]
    
    for template_name in templates:
        try:
            template = get_template(template_name)
            template_source = template.source
            
            # Check for {% load static %}
            if '{%' + ' load static ' + '%}' in template_source:
                print(f"   ✅ {template_name} has load static tag")
                success.append(f"Template loads static: {template_name}")
            else:
                print(f"   ❌ {template_name} missing load static tag")
                issues.append(f"Template missing static load: {template_name}")
            
            # Check for CSS references
            css_files = ['login.css', 'register.css']
            for css_file in css_files:
                if css_file in template_source:
                    print(f"   ✅ {template_name} references {css_file}")
                    success.append(f"Template references CSS: {template_name} -> {css_file}")
            
            # Check for JS references  
            js_files = ['login.js', 'register.js']
            for js_file in js_files:
                if js_file in template_source:
                    print(f"   ✅ {template_name} references {js_file}")
                    success.append(f"Template references JS: {template_name} -> {js_file}")
                    
        except Exception as e:
            print(f"   ❌ Error loading template {template_name}: {e}")
            issues.append(f"Template error {template_name}: {e}")
    
    # 5. Check file content
    print("\n5. FILE CONTENT CHECK:")
    css_files = [
        ('blog/static/css/login.css', '.login-container'),
        ('blog/static/css/register.css', '.register-container')
    ]
    
    for file_path, expected_class in css_files:
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if expected_class in content:
                        print(f"   ✅ {file_path} contains {expected_class}")
                        success.append(f"CSS content valid: {file_path}")
                    else:
                        print(f"   ❌ {file_path} missing {expected_class}")
                        issues.append(f"CSS content invalid: {file_path}")
        except Exception as e:
            print(f"   ❌ Error reading {file_path}: {e}")
            issues.append(f"File read error {file_path}: {e}")
    
    # 6. Directory structure check
    print("\n6. DIRECTORY STRUCTURE CHECK:")
    required_dirs = [
        'blog/static',
        'blog/static/css', 
        'blog/static/js',
        'blog/templates',
        'blog/templates/registration',
        'static',
        'static/css',
        'static/js'
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"   ✅ Directory: {dir_path}")
            success.append(f"Directory exists: {dir_path}")
        else:
            print(f"   ❌ Missing directory: {dir_path}")
            issues.append(f"Missing directory: {dir_path}")
    
    # Summary
    print("\n" + "="*50)
    print("📊 SUMMARY:")
    print(f"✅ Successful checks: {len(success)}")
    print(f"❌ Issues found: {len(issues)}")
    
    if issues:
        print("\n🚨 ISSUES TO FIX:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    
    if success:
        print("\n✅ WORKING COMPONENTS:")
        for i, item in enumerate(success[:5], 1):  # Show first 5
            print(f"   {i}. {item}")
        if len(success) > 5:
            print(f"   ... and {len(success) - 5} more")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    if not issues:
        print("   🎉 All checks passed! Static files are properly implemented.")
    else:
        print("   🔧 Fix the issues listed above")
        print("   📁 Ensure all static files exist in both blog/static/ and static/ directories")
        print("   🔗 Verify templates properly reference static files with {% static %} tag")
        print("   ⚙️ Check Django settings for STATIC_URL and STATICFILES_DIRS")
    
    return len(issues) == 0

if __name__ == '__main__':
    success = check_static_files()
    sys.exit(0 if success else 1)

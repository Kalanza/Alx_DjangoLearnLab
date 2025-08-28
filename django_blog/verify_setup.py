#!/usr/bin/env python3
"""
Project verification script for Django Blog
This script checks that all required components are in place.
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists and print status"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description}: {filepath} (MISSING)")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists and print status"""
    if os.path.isdir(dirpath):
        print(f"✓ {description}: {dirpath}")
        return True
    else:
        print(f"✗ {description}: {dirpath} (MISSING)")
        return False

def main():
    print("Django Blog Project Structure Verification")
    print("=" * 50)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    all_good = True
    
    # Core Django files
    files_to_check = [
        (os.path.join(base_dir, "manage.py"), "Django management script"),
        (os.path.join(base_dir, "db.sqlite3"), "SQLite database"),
        (os.path.join(base_dir, "README.md"), "Project documentation"),
        (os.path.join(base_dir, "requirements.txt"), "Python dependencies"),
        (os.path.join(base_dir, ".gitignore"), "Git ignore file"),
    ]
    
    # Project files
    files_to_check.extend([
        (os.path.join(base_dir, "blog_project", "settings.py"), "Project settings"),
        (os.path.join(base_dir, "blog_project", "urls.py"), "Main URL configuration"),
        (os.path.join(base_dir, "blog_project", "wsgi.py"), "WSGI configuration"),
    ])
    
    # Blog app files
    files_to_check.extend([
        (os.path.join(base_dir, "blog", "models.py"), "Blog models"),
        (os.path.join(base_dir, "blog", "views.py"), "Blog views"),
        (os.path.join(base_dir, "blog", "urls.py"), "Blog URL patterns"),
        (os.path.join(base_dir, "blog", "admin.py"), "Admin configuration"),
        (os.path.join(base_dir, "blog", "apps.py"), "App configuration"),
    ])
    
    # Template files
    files_to_check.extend([
        (os.path.join(base_dir, "blog", "templates", "blog", "base.html"), "Base template"),
        (os.path.join(base_dir, "blog", "templates", "blog", "home.html"), "Home template"),
    ])
    
    # Static files
    files_to_check.extend([
        (os.path.join(base_dir, "blog", "static", "blog", "css", "style.css"), "CSS stylesheet"),
        (os.path.join(base_dir, "blog", "static", "blog", "js", "main.js"), "JavaScript file"),
    ])
    
    # Management command
    files_to_check.extend([
        (os.path.join(base_dir, "blog", "management", "commands", "create_sample_posts.py"), "Sample posts command"),
    ])
    
    # Check directories
    directories_to_check = [
        (os.path.join(base_dir, "blog"), "Blog app directory"),
        (os.path.join(base_dir, "blog_project"), "Project directory"),
        (os.path.join(base_dir, "blog", "migrations"), "Migrations directory"),
        (os.path.join(base_dir, "blog", "static"), "Static files directory"),
        (os.path.join(base_dir, "blog", "templates"), "Templates directory"),
        (os.path.join(base_dir, "blog", "management"), "Management commands directory"),
    ]
    
    print("\nChecking Files:")
    print("-" * 30)
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_good = False
    
    print("\nChecking Directories:")
    print("-" * 30)
    for dirpath, description in directories_to_check:
        if not check_directory_exists(dirpath, description):
            all_good = False
    
    print("\n" + "=" * 50)
    if all_good:
        print("✓ All components are in place! Project setup is complete.")
        print("\nTo start the development server, run:")
        print("python manage.py runserver")
        print("\nTo create sample posts, run:")
        print("python manage.py create_sample_posts")
    else:
        print("✗ Some components are missing. Please check the setup.")
    
    print("\nProject Features:")
    print("- Django 5.2.5 project setup")
    print("- Blog app with Post model")
    print("- Responsive Bootstrap-based templates")
    print("- Static files configuration")
    print("- Admin interface")
    print("- Sample data management command")
    print("- Complete documentation")

if __name__ == "__main__":
    main()

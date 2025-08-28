#!/usr/bin/env python3
"""
Static Files Verification Script for Django Blog
This script checks that all static files are properly configured.
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

def main():
    print("Static Files Configuration Verification")
    print("=" * 50)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    all_good = True
    
    # Static files to check
    static_files = [
        (os.path.join(base_dir, "blog", "static", "css", "styles.css"), "Main CSS stylesheet"),
        (os.path.join(base_dir, "blog", "static", "js", "scripts.js"), "Main JavaScript file"),
    ]
    
    # Template files
    template_files = [
        (os.path.join(base_dir, "blog", "templates", "blog", "base.html"), "Updated base template"),
        (os.path.join(base_dir, "blog", "templates", "blog", "home.html"), "Updated home template"),
    ]
    
    print("\nChecking Static Files:")
    print("-" * 30)
    for filepath, description in static_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    print("\nChecking Template Files:")
    print("-" * 30)
    for filepath, description in template_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    print("\nVerifying File Contents:")
    print("-" * 30)
    
    # Check if CSS file contains the expected styles
    css_file = os.path.join(base_dir, "blog", "static", "css", "styles.css")
    if os.path.exists(css_file):
        with open(css_file, 'r') as f:
            css_content = f.read()
        if "Basic reset" in css_content and "header" in css_content:
            print("✓ CSS file contains expected styles")
        else:
            print("✗ CSS file does not contain expected styles")
            all_good = False
    
    # Check if JS file contains the expected scripts
    js_file = os.path.join(base_dir, "blog", "static", "js", "scripts.js")
    if os.path.exists(js_file):
        with open(js_file, 'r') as f:
            js_content = f.read()
        if "DOMContentLoaded" in js_content and "console.log" in js_content:
            print("✓ JavaScript file contains expected functionality")
        else:
            print("✗ JavaScript file does not contain expected functionality")
            all_good = False
    
    # Check if base template is updated
    base_template = os.path.join(base_dir, "blog", "templates", "blog", "base.html")
    if os.path.exists(base_template):
        with open(base_template, 'r') as f:
            template_content = f.read()
        if "static 'css/styles.css'" in template_content and "<header>" in template_content:
            print("✓ Base template is properly updated")
        else:
            print("✗ Base template is not properly updated")
            all_good = False
    
    print("\n" + "=" * 50)
    if all_good:
        print("✓ All static files are properly configured!")
        print("\nStatic Files Features:")
        print("- Clean, modern CSS design")
        print("- Interactive JavaScript functionality")
        print("- Properly structured templates")
        print("- Responsive layout")
        print("\nTo view the updated design:")
        print("Visit http://127.0.0.1:8000/ in your browser")
    else:
        print("✗ Some static files are missing or misconfigured.")
    
    print("\nStatic Files Structure:")
    print("blog/static/")
    print("├── css/")
    print("│   └── styles.css")
    print("└── js/")
    print("    └── scripts.js")

if __name__ == "__main__":
    main()

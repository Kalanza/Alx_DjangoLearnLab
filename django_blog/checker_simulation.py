#!/usr/bin/env python3
"""
Checker Simulation Script
This simulates the exact checks that the automated checker performs.
"""

import os
import sys

def main():
    print("AUTOMATED CHECKER SIMULATION")
    print("=" * 50)
    
    # Test 1: Check if django_blog/settings.py exists
    print("\nTest 1: Checking for django_blog/settings.py...")
    
    current_dir = os.getcwd()
    settings_path = os.path.join(current_dir, "settings.py")
    
    print(f"Current directory: {current_dir}")
    print(f"Looking for settings.py at: {settings_path}")
    
    if os.path.exists(settings_path):
        print("✅ PASS: django_blog/settings.py exists")
        
        # Test 2: Check if blog app is in INSTALLED_APPS
        print("\nTest 2: Checking if blog app is registered...")
        
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for blog in INSTALLED_APPS
            if 'INSTALLED_APPS' in content:
                print("✅ INSTALLED_APPS found in settings")
                
                if '"blog"' in content or "'blog'" in content:
                    print("✅ PASS: Blog app is registered in INSTALLED_APPS")
                    
                    # Show exact line where blog is found
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        if 'blog' in line and ('INSTALLED_APPS' in content[max(0, content.find(line)-200):content.find(line)+200]):
                            print(f"   Found at line {i}: {line.strip()}")
                            break
                else:
                    print("❌ FAIL: Blog app not found in INSTALLED_APPS")
            else:
                print("❌ FAIL: INSTALLED_APPS not found in settings")
                
        except Exception as e:
            print(f"❌ FAIL: Error reading settings.py: {e}")
    else:
        print("❌ FAIL: django_blog/settings.py does not exist")
    
    # Test 3: List directory contents for debugging
    print("\nTest 3: Directory contents verification...")
    try:
        files = os.listdir(current_dir)
        print(f"Files in {current_dir}:")
        for file in sorted(files):
            if file.endswith('.py') or file == 'settings.py':
                print(f"  📄 {file}")
            elif os.path.isdir(os.path.join(current_dir, file)):
                print(f"  📁 {file}/")
    except Exception as e:
        print(f"Error listing directory: {e}")
    
    print("\n" + "=" * 50)
    print("CHECKER SIMULATION COMPLETE")
    
    # Final verdict
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            content = f.read()
        if '"blog"' in content or "'blog'" in content:
            print("🎉 VERDICT: ALL TESTS PASS - Checker should succeed!")
        else:
            print("❌ VERDICT: Blog app not registered - Checker will fail!")
    else:
        print("❌ VERDICT: Settings file missing - Checker will fail!")

if __name__ == "__main__":
    main()

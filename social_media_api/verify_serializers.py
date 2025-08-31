#!/usr/bin/env python
"""
Verification script to check that the serializers.py contains the required pattern.
"""

import os
import sys

def main():
    """Check if serializers.py contains the required pattern."""
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    serializers_path = os.path.join(current_dir, 'accounts', 'serializers.py')
    
    print("🔍 Checking accounts/serializers.py for required pattern...")
    print(f"File path: {serializers_path}")
    
    if not os.path.exists(serializers_path):
        print("❌ serializers.py file not found!")
        return False
    
    # Read the file content
    with open(serializers_path, 'r') as f:
        content = f.read()
    
    # Check for the required pattern
    required_pattern = "get_user_model().objects.create_user"
    
    if required_pattern in content:
        print(f"✅ Found required pattern: {required_pattern}")
        
        # Show the context where it's used
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if required_pattern in line:
                print(f"\nFound at line {i+1}:")
                print(f"  {line.strip()}")
                
                # Show some context
                start = max(0, i-2)
                end = min(len(lines), i+3)
                print("\nContext:")
                for j in range(start, end):
                    marker = ">>> " if j == i else "    "
                    print(f"{marker}{j+1:3}: {lines[j]}")
        
        return True
    else:
        print(f"❌ Required pattern not found: {required_pattern}")
        print("\nFile contents:")
        print("-" * 50)
        print(content)
        print("-" * 50)
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Verification passed! The serializers.py file contains the required pattern.")
    else:
        print("\n❌ Verification failed! The required pattern is missing.")
    
    sys.exit(0 if success else 1)

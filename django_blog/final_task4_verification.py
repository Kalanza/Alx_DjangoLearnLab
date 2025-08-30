#!/usr/bin/env python3
"""
Final verification test for Task 4: Tagging and Search Functionality
This script validates all the requirements are met.
"""

import os
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')

def check_requirements():
    """Check all Task 4 requirements"""
    
    print("🔍 Task 4 Requirements Verification")
    print("=" * 50)
    
    try:
        import django
        django.setup()
        
        # 1. Check django-taggit in settings
        from django.conf import settings
        if 'taggit' in settings.INSTALLED_APPS:
            print("✅ Step 1: taggit is in INSTALLED_APPS")
        else:
            print("❌ Step 1: taggit is NOT in INSTALLED_APPS")
            return False
        
        # 2. Check TaggableManager in Post model
        from blog.models import Post
        from taggit.managers import TaggableManager
        
        if hasattr(Post, 'tags') and isinstance(Post.tags, TaggableManager):
            print("✅ Step 1: Post model has TaggableManager for tags")
        else:
            print("❌ Step 1: Post model does not have TaggableManager")
            return False
        
        # 3. Check TagWidget in forms
        with open('blog/forms.py', 'r') as f:
            forms_content = f.read()
            if 'TagWidget()' in forms_content:
                print("✅ Step 2: forms.py contains TagWidget()")
            else:
                print("❌ Step 2: forms.py does not contain TagWidget()")
                return False
        
        # 4. Check search functionality
        from blog.forms import SearchForm
        print("✅ Step 3: SearchForm is implemented")
        
        # 5. Check search views
        from blog.views import SearchResultsView, PostsByTagView, TagListView
        print("✅ Step 3: Search views are implemented")
        
        # 6. Check URL patterns
        with open('blog/urls.py', 'r') as f:
            urls_content = f.read()
            if 'search/' in urls_content and 'tags/' in urls_content:
                print("✅ Step 5: URL patterns for search and tags are configured")
            else:
                print("❌ Step 5: URL patterns missing")
                return False
        
        # 7. Check templates exist
        import os
        template_files = [
            'blog/templates/blog/search_results.html',
            'blog/templates/blog/posts_by_tag.html',
            'blog/templates/blog/tag_list.html'
        ]
        
        for template in template_files:
            if os.path.exists(template):
                print(f"✅ Step 4: Template exists: {template}")
            else:
                print(f"❌ Step 4: Template missing: {template}")
                return False
        
        print("\n" + "=" * 50)
        print("🎉 ALL REQUIREMENTS MET!")
        print("Task 4: Tagging and Search Functionality - COMPLETE")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

if __name__ == '__main__':
    success = check_requirements()
    if success:
        print("\n✅ Your implementation is ready for evaluation!")
    else:
        print("\n❌ Some requirements are not met. Please review the implementation.")
        sys.exit(1)

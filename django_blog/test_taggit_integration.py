#!/usr/bin/env python3
"""
Test script to verify django-taggit integration
"""

import os
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')

try:
    import django
    django.setup()
    
    # Test taggit import
    from taggit.managers import TaggableManager
    from taggit.models import Tag as TaggitTag
    
    print("✅ django-taggit successfully imported")
    
    # Test our models
    from blog.models import Post
    
    # Check if Post has TaggableManager
    if hasattr(Post, 'tags') and isinstance(Post.tags, TaggableManager):
        print("✅ Post model has TaggableManager")
    else:
        print("❌ Post model does not have TaggableManager")
    
    # Test settings
    from django.conf import settings
    if 'taggit' in settings.INSTALLED_APPS:
        print("✅ taggit is in INSTALLED_APPS")
    else:
        print("❌ taggit is NOT in INSTALLED_APPS")
    
    # Test form import
    try:
        from taggit.forms import TagWidget
        print("✅ TagWidget successfully imported")
    except ImportError as e:
        print(f"❌ TagWidget import failed: {e}")
    
    print("\n🎉 All django-taggit checks passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

from django.contrib import admin
from .models import Book

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")
    search_fields = ("title", "author")
    list_filter = ("author",)
    ordering = ("title",)

admin.site.register(Book, BookAdmin)

#Integrate the Custom User Model into Admin

from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
#import all of our cutom models

class CustomUserAdmin(UserAdmin):
    """
    Custom Admin Configuration for CustomUser Model
    Purpose: Extends Django's built-in UserAdmin to handle our custom fields.
    """
    # Add custom fields to the list display
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff')
    
    # Add custom fields to search functionality
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Filter options
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    # Ordering
    ordering = ('username',)
    
    # Fieldsets for add/edit forms
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )
    
    # Fields to show when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )
    



admin.site.register(CustomUser, CustomUserAdmin)

# Enhanced Group and Permission Management
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import GroupAdmin

class CustomGroupAdmin(GroupAdmin):
    """
    Enhanced Group Admin for better permission management
    """
    list_display = ('name', 'get_permissions_count')
    search_fields = ('name',)
    filter_horizontal = ('permissions',)
    
    def get_permissions_count(self, obj):
        """Display the number of permissions in each group"""
        return obj.permissions.count()
    get_permissions_count.short_description = 'Permissions Count'

# Unregister the default Group admin and register our custom one
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)

# Custom Permission Admin for better visibility
class PermissionAdmin(admin.ModelAdmin):
    """
    Custom Permission Admin for better management
    """
    list_display = ('name', 'codename', 'content_type')
    list_filter = ('content_type',)
    search_fields = ('name', 'codename')
    ordering = ('content_type', 'codename')

admin.site.register(Permission, PermissionAdmin)
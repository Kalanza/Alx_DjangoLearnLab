from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser, UserProfile

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author')

# Custom User Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Fields to display in the user list
    list_display = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    
    # Fields to show when editing a user
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )
    
    # Fields to show when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )

# UserProfile Admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email']

admin.site.register(Book, BookAdmin)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Author, Book, Library, Librarian, UserProfile

class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for CustomUser model.
    """
    # Fields to display in the admin list view
    list_display = ('email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_active', 'date_joined')
    
    # Fields that can be searched
    search_fields = ('email', 'first_name', 'last_name')
    
    # Filters in the right sidebar
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    # Order by email instead of username
    ordering = ('email',)
    
    # Fieldsets for the detailed user form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth', 'profile_photo'),
        }),
    )
    
    # Remove username from readonly fields since we're using email
    readonly_fields = ('date_joined', 'last_login')

class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserProfile model.
    """
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')

class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for Book model.
    """
    list_display = ('title', 'author')
    list_filter = ('author',)
    search_fields = ('title', 'author__name')

class LibraryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Library model.
    """
    list_display = ('name',)
    filter_horizontal = ('books',)  # Makes it easier to manage many-to-many relationships

class LibrarianAdmin(admin.ModelAdmin):
    """
    Admin configuration for Librarian model.
    """
    list_display = ('name', 'library')
    search_fields = ('name', 'library__name')

# Register the CustomUser with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)

# Register other models with their custom admin classes
admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Librarian, LibrarianAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

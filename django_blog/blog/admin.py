from django.contrib import admin
from .models import Post, Comment

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'content')
    ordering = ('-published_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'content_preview')
    list_filter = ('created_at', 'author', 'post')
    search_fields = ('content', 'author__username', 'post__title')
    ordering = ('-created_at',)
    raw_id_fields = ('post',)

    def content_preview(self, obj):
        """Show a preview of the comment content."""
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

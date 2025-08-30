from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Return the URL for the tag detail view"""
        return reverse('posts-by-tag', kwargs={'tag_name': self.name})

    class Meta:
        ordering = ['name']


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Return the URL for the post detail view"""
        return reverse('post-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-published_date']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

    def get_absolute_url(self):
        """Return the URL for the post detail view with comment anchor"""
        return reverse('post-detail', kwargs={'pk': self.post.pk}) + f'#comment-{self.pk}'

    class Meta:
        ordering = ['created_at']

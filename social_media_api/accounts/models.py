from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Adds additional fields for social media functionality.
    """
    bio = models.TextField(max_length=500, blank=True, help_text="A brief description about the user")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, help_text="User's profile picture")
    followers = models.ManyToManyField(
        'self', 
        through='Follow',
        related_name='following',
        symmetrical=False,
        blank=True,
        help_text="Users who follow this user"
    )
    
    def __str__(self):
        return self.username

class Follow(models.Model):
    """
    Intermediate model for user following relationships.
    """
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower_relationships')
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following_relationships')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
        
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    class Meta:
        ordering = ['title']

# Custom User Model extending AbstractUser
# AbstractUser already includes a manager, so no custom manager needed

class CustomUser(AbstractUser):
    # Add the required custom fields
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    def __str__(self):
        return self.username

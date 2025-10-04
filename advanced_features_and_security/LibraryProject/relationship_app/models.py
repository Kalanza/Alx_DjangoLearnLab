from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

User = get_user_model()

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=20)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"

class Library(models.Model):
    name = models.CharField(max_length=50)
    books = models.ManyToManyField(Book)
    
    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=50)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
   

# The '@receiver' decorator connects this function to the post_save signal.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Called after a User model is saved.
    """
    # 'created' is a boolean: True if the record was just created, False if it was updated.
    if created:
        # If the user was just created, automatically create a UserProfile
        UserProfile.objects.create(user=instance)

# This function is not strictly needed for creation, but it's good practice
# to automatically save the profile when the User object is saved.
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Called after a User model is saved to ensure the corresponding 
    UserProfile is also saved if it already exists.
    """
    # Use instance.userprofile.save() if the profile is guaranteed to exist
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        # Pass silently if the profile doesn't exist (e.g., initial creation)
        pass
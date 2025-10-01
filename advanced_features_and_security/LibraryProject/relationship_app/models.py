from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


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
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
    
    def __str__(self):
        return f"{self.user.email} - {self.role}"
   

# The '@receiver' decorator connects this function to the post_save signal.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Called after a CustomUser model is saved.
    """
    # 'created' is a boolean: True if the record was just created, False if it was updated.
    if created:
        # If the user was just created, automatically create a UserProfile
        UserProfile.objects.create(user=instance)

# This function is not strictly needed for creation, but it's good practice
# to automatically save the profile when the User object is saved.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Called after a CustomUser model is saved to ensure the corresponding 
    UserProfile is also saved if it already exists.
    """
    # Use instance.userprofile.save() if the profile is guaranteed to exist
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        # Pass silently if the profile doesn't exist (e.g., initial creation)
        pass


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for CustomUser model.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        
        # Normalize the email address
        email = self.normalize_email(email)
        
        # Set default values for extra fields
        extra_fields.setdefault('is_active', True)
        
        # Create the user instance
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        # Set required fields for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    # Override the username field to remove unique constraint
    username = models.CharField(max_length=150, blank=True, null=True)
    
    # Override the email field to make it unique and required
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    # Add the custom manager
    objects = CustomUserManager()
    
    # Set email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Remove 'username' from required fields since we're using email
    
    def __str__(self):
        return self.email

# ...existing code... (Author, Book, Library, Librarian models)
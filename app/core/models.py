"""
Database models.
"""
from django.conf import settings
from django.db import models #it has the basic django model fields
from django.contrib.auth.models import (
    AbstractBaseUser, #to define custom User class
    BaseUserManager,  #to manage creating different type of users
    PermissionsMixin, #adds fields and methods to handle persmissions eg is_superuser
)
# Create your models here.

class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self,email,password = None, **extra_fields):
        """Create, save and return a  new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields) #creates a user instance self.model is connected to User since objects = UsrManager
        user.set_password(password) #hashes plain text password
        user.save(using=self._db) #returns created user object

        return user
    
    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password) #reuses create user to emnsure email normalization and pass hashing
        user.is_staff = True #admin flag
        user.is_superuser = True #admin flag
        user.save(using=self._db) #returns superuser object

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique= True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default=False)


    objects = UserManager() #assigns the custom manager to the objects attribute
                            #enables User.objects.create_user

    USERNAME_FIELD = 'email' #Specifies which field should be used as the unique identifier for authentication.


class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, #cascade = delete all linked if user deleted
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True) #optional
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True) #blank = optional

    def __str__(self):
        return self.title
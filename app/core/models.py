from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fileds):
        """Create and saves a new user"""
        if not email:
            raise ValueError('User  must provide an email adress')

        # self.model() -> creates a new user model
        user = self.model(email=self.normalize_email(email), **extra_fileds)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create a new superuser profile"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system that supports using email
    instead of  username"""

    # Database fields: auth
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    # Database fields: permissions
    # Determine if a user's profile is active
    is_active = models.BooleanField(default=True)
    # Determine if a active user is part of the staff,
    #  who can access django admin
    is_staff = models.BooleanField(default=False)
    # is_superuser is inherited from PermissionsMixin

    # manager required for django cli
    objects = UserManager()

    # when authenticating we should provide email as username
    USERNAME_FIELD = 'email'

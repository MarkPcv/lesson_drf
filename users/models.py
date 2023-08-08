from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {
    'null': True,
    'blank': True,
}


class UserRoles(models.TextChoices):
    MEMBER = 'member'
    MODERATOR = 'moderator'


class User(AbstractUser):
    """
    Stores a single user entry for authenticated users.
    """
    username = None
    email = models.EmailField(unique=True, verbose_name='email')

    phone = models.CharField(max_length=35, verbose_name='phone',
                             **NULLABLE)

    city = models.CharField(max_length=50, verbose_name='city', **NULLABLE)
    avatar = models.ImageField(**NULLABLE, verbose_name='avatar')

    # Role for permissions
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

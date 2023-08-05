from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {
    'null': True,
    'blank': True,
}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')

    phone = models.CharField(max_length=35, verbose_name='phone',
                             **NULLABLE)

    city = models.CharField(max_length=50, verbose_name='city', **NULLABLE)
    avatar = models.ImageField(**NULLABLE, verbose_name='avatar')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

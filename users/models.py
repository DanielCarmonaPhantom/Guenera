from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    suscription = models.CharField(blank=False, default='A', max_length=2)

    worktable_active = models.IntegerField(blank=True, null=True)

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract =True

class User(AbstractUser, TimeStampedModel):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
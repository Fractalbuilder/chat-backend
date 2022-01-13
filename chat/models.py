from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Message(models.Model):
    userId = models.IntegerField()
    username = models.CharField(max_length=20)
    text = models.CharField(max_length=200)
    datetime = models.CharField(max_length=30)

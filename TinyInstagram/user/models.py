from django.contrib.auth.models import AbstractUser
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    phone_number = models.CharField(max_length=11, null=True)
    full_name = models.CharField(max_length=50, null=True)
    date_of_birth = models.DateField(null=True)
    #following = models.ManyToManyField('self',through='Contact', related_name='following', symmetrical=False)
    bio = models.TextField(null=True)

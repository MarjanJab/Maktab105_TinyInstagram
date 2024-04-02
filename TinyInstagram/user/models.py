from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


# class User(models.Model):
#     username = models.CharField(max_length=20, unique=True)
#     password = models.CharField(max_length=20)
#     email = models.EmailField()
#     phone_number = models.CharField(max_length=11, null=True)
#     full_name = models.CharField(max_length=50, null=True)


class Profile(models.Model):
    user = models.ForeignKey(User, related_name='rel_to_profile', on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(null=True)
    date_of_birth = models.DateField(null=True)


class Follow(models.Model):
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)


class OTP(models.Model):
    user = models.ForeignKey(User, related_name='send_otp', on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    expiration_date = models.DateField(null=True)

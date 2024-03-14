from django.db import models
from django.utils import timezone
from user.models import User


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts", verbose_name="نویسنده")
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    dislikes = models.ManyToManyField(User, related_name="disliked_posts", blank=True)
    total_likes = models.PositiveIntegerField(default=0)
    total_dislikes = models.PositiveIntegerField(default=0)
    #tags


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image_url = models.ImageField(upload_to="post_images/")

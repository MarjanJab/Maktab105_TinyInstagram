from django.db import models

from post.models import Post
from user.models import User


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=250,null=True,blank=True)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

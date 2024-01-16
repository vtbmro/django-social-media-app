from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import datetime
import json

class User(AbstractUser):
    pass

class Post(models.Model):
# model for the Post should include: text, user, date

    # text
    text_content = models.TextField(max_length=256, blank=False)
    
    # user_id who created the post
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user")

    # date, hour, minute
    date = models.DateTimeField(auto_now_add=True)

    # number of likes 
    likes = models.IntegerField(default=0)
    
    # List of user that have liked the post
    liked_by = models.ManyToManyField(User, related_name="liked_by")


class Follower (models.Model):
# model to keep track of who follows who

    # who the person is following 
    follows = models.ForeignKey(User,on_delete=models.CASCADE, related_name="followed")

    # the follower in question
    follower = models.ForeignKey(User,on_delete=models.CASCADE,  related_name="follower")


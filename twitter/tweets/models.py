from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)

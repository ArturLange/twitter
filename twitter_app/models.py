import hashlib

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)

    def gravatar_url(self):
        return "http://www.gravatar.com/avatar/%s?s=50" % hashlib.md5(self.user.email).hexdigest()


class PostManager(models.Manager):
    def get_by_user_id(self, user_id):
        return self.filter(creator_id=user_id)


class Post(models.Model):
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)
    objects = PostManager()

    def __str__(self):
        return str(self.creator) + self.content


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

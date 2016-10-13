from django.db import models

from threads.models import Thread
from user.models import User


class Forum(models.Model):
    """
    Just a forum
    """
    name = models.CharField(max_length=120, unique=True, db_index=True)
    short_name = models.CharField(max_length=60, unique=True, db_index=True)

    user = models.ForeignKey(User, related_name='forum_list')

    def __str__(self):
        return self.short_name


class Post(models.Model):
    """
    Post in forum
    """
    user = models.ForeignKey(User)
    forum = models.ForeignKey(Forum)
    thread = models.ForeignKey(Thread)

    message = models.TextField()

    date = models.DateTimeField()

    # Optional
    parent = models.ForeignKey('self', related_name='child_post_list', blank=True, null=True)
    isApproved = models.BooleanField(blank=True, default=False)
    isHighlighted = models.BooleanField(blank=True, default=False)
    isEdited = models.BooleanField(blank=True, default=False)
    isSpam = models.BooleanField(blank=True, default=False)
    isDeleted = models.BooleanField(blank=True, default=False)

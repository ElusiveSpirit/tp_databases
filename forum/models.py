from django.db import models

from user.models import User


class Forum(models.Model):
    """
    Just a forum
    """
    user = models.ForeignKey(User, related_name='forum_list')

    name = models.CharField(max_length=120, unique=True, db_index=True)
    short_name = models.CharField(max_length=60, unique=True, db_index=True)

    def __str__(self):
        return self.short_name


class Thread(models.Model):
    """
    Model for forum thread
    """
    forum = models.ForeignKey(Forum, related_name='thread_list')
    user = models.ForeignKey(User, related_name='thread_list')

    title = models.CharField(max_length=120)
    message = models.TextField()
    slug = models.CharField(max_length=40, unique=True)

    isClosed = models.BooleanField()
    isDeleted = models.BooleanField(blank=True, default=False)

    date = models.DateTimeField()

    def __str__(self):
        return self.slug


class Post(models.Model):
    """
    Post in forum
    """
    user = models.ForeignKey(User)
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

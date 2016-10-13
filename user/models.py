from django.db import models


class User(models.Model):
    """
    Main user model
    """
    username = models.CharField(max_length=40, db_index=True)
    email = models.CharField(max_length=100, unique=True, db_index=True)
    about = models.TextField()
    name = models.CharField(max_length=40)

    isAnonymous = models.BooleanField(blank=True, default=False)

    following = models.ManyToManyField('self', related_name='followers')

    def get_following_count(self):
        return self.following.count()

    def get_followers_count(self):
        return self.followers.count()

    def __str__(self):
        return self.email

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

    def __str__(self):
        return self.email

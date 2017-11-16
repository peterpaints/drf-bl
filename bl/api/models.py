from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver


class Bucketlist(models.Model):
    """Model the bucketlist table."""

    name = models.CharField(max_length=255, unique=True, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', related_name="bucketlists",
                                   on_delete=models.CASCADE)

    def __str__(self):
        """Return representation of the table."""
        return "{}".format(self.name)


class Item(models.Model):
    """Model the bucketlist item table."""

    name = models.CharField(max_length=255, unique=True, blank=False)
    bucketlist = models.ForeignKey(Bucketlist, related_name="items",
                                   on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        """Return representation of the table."""
        return "{}".format(self.name)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.object.create(user=instance)

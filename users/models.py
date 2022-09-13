from django.db import models
from django.contrib.auth.models import User
from subscription.models import Subscription


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='new_user'
    )

    avatar = models.ImageField(
        default='default.jpg',
        upload_to='profile_images'
    )
    bio = models.TextField()
    subscription = models.ManyToManyField(Subscription, blank=True)

    def __str__(self):
        return self.user.username

from django.db import models
from django.contrib.auth import get_user_model



class Profile(models.Model):
    User = get_user_model()
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    avatar = models.ImageField(
        default='default.jpeg',
        upload_to='profile_images',
        blank=True
    )
    bio = models.TextField()

    def __str__(self):
        return self.user.username

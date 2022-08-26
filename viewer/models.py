from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=100, blank=True, null=True, default=None)
    home_airport = models.ForeignKey('search.Airport', on_delete=models.DO_NOTHING, blank=True, null=True)


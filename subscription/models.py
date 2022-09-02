from constants import CURRENCIES

from django.contrib.auth.models import User
from django.db import models

from search.models import Search

class Subscription(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price_to = models.PositiveIntegerField(blank=True, null=True)
    curr = models.CharField(max_length=3, choices=CURRENCIES, default='EUR')
    email = models.EmailField()



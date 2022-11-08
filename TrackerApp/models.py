from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Stock(models.Model):
    symbol = models.CharField(max_length=255, null=True, blank=True, unique=True)

    def __str__(self):
        return self.symbol

class WatchList(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    stocks = models.ManyToManyField(Stock, blank=True)
    desc = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

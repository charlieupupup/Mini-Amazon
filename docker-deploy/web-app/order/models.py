from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class order(models.Model):
    # each record: one kind of products in one package
    user = models.ForeignKey(User, on_delete=models.CASCADE) # user
    x = models.IntegerField(default=-1, verbose_name='Destination X Value')  # user address
    y = models.IntegerField(default=-1, verbose_name='Destination Y Value')  # user address
    pkgid = models.IntegerField(default=-1) # package id & Tracking num & Ship id
    pid = models.IntegerField(default=-1, verbose_name='Product ID')  # product id
    count = models.IntegerField(default=-1, verbose_name='Product Count')  # product quantity
    whid = models.IntegerField(default=0)  # warehouse id
    truckid = models.IntegerField(default=-1) # truck id
    arrived = models.BooleanField(default=False)
    ready = models.BooleanField(default=False)
    loaded = models.BooleanField(default=False)

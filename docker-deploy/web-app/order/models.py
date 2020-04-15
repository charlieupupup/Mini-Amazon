from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class order(models.Model):
    # each record: one kind of products in one package
    user = models.ForeignKey(User, on_delete=models.CASCADE) # user
    x = models.IntegerField(default=-1)  # user address
    y = models.IntegerField(default=-1)  # user address
    pkgid = models.IntegerField(default=-1) # package id & Tracking num & Ship id
    pid = models.IntegerField(default=-1)  # product id
    count = models.IntegerField(default=-1)  # product quantity

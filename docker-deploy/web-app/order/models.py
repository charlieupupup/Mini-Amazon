from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class order(models.Model):
    # each record: one kind of products in one package
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user
    x = models.IntegerField(
        default=-1, verbose_name='Destination X Value')  # user address
    y = models.IntegerField(
        default=-1, verbose_name='Destination Y Value')  # user address
    # package id & Tracking num & Ship id
    pkgid = models.IntegerField(default=-1)
    pid = models.IntegerField(
        default=-1, verbose_name='Product ID')  # product id
    count = models.IntegerField(
        default=-1, verbose_name='Product Count')  # product quantity
    whid = models.IntegerField(default=0)  # warehouse id
    truckid = models.IntegerField(default=-1)  # truck id
    status = models.CharField(max_length=100, default="", blank=True)
    email = models.EmailField(max_length=254, default='xxx@qq.com')
